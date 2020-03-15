import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import threading
import sys

import Rigol_Lib.RigolSCPI as rs
import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp
import TCPconnection.TCPListener as tl

# from Rigol_util import RigolRespProc as rrp
from Rigol_util import channelDataKeeper as cld
# from Rigol_util import Rigol_plotter as Rigol_plotter
from Rigol_util import RigolCommander as rc
from TransactionMeans import DoorBell as db 
from decoder import FFTModule
from decoder import SineCreator
import time
import queue
from TransactionMeans import LimitedQueue
from debug import debug_instr as dbg
from Rigol_util import Oscilloscope_model
from Gui import controlAndProcess
from decoder import FFTController

class ConsoleControl: 
    """ 
        A wrapper class to put the console application and its functionality 
        in a single object. This class launches threads to handle tcp connection. 

        Can be used as the main thread when using none-gui applications
        Can be launched in a second thread (the run method) when using gui applications

    """
    ## Archaic: better to be implemented using Queue.queue (thread safe)
    global doorbell_obj # doorbell objet is used between the thread running this class and the thread handling tcp connections
    

    command_counter = 0 
   
    data_processor = controlAndProcess.ProcessModel()
    # processor_type = controlAndProcess.fftprocess
    processor_type = FFTController.FFTObserver

    ## doorbell_queue: A better implementation of of doorbell obj
    # doorbell_queue:LimitedQueue = LimitedQueue.LimitedQueue(10)

    ## oscilloscope model holds the state of the oscilloscope at each time
    my_oscilloscope:Oscilloscope_model.Oscilloscope = Oscilloscope_model.Oscilloscope(avaialable_ch=[rs.RIGOL_CHANNEL_IDX.CH3, 
                                                                rs.RIGOL_CHANNEL_IDX.CH4])

    ## maximum queue sizes: used for limited queue
    queue_max_size = 10
    
    ## A queue to hold all responses (preamable, data and fft) received over tcp
    tcp_resp_queue = LimitedQueue.LimitedQueue(queue_max_size)

    ## Where is it used ? 
    fft_resp_queue = LimitedQueue.LimitedQueue(queue_max_size)

    ## A queue to hold tcp preamble responses (message passing between this obj thread and gui)
    tcp_preamble_queue = LimitedQueue.LimitedQueue(queue_max_size)

    ## A queue to hold tcp response data
    tcp_resp_data_queue = LimitedQueue.LimitedQueue(queue_max_size)
    

    def __init__(self):
        # create doorbell object for message passing between main thread
        # and the single thread
        self.doorbell_obj = db.DoorBell()

        ## create commander object to manage generation of commands
        self.rigol_commander = rc.RigolCommander()

        ## create tcp object: manages send, receive, connection
        self.tcp_connection = tcp.TCPcomm()

        self.__pause_tcp_conn = False

        self.data_processor.connect_f2q(self.data_processor.rawDataRead ,
                                        self.tcp_resp_data_queue)
        
        self.data_processor.setProcessor(self.processor_type,
                                            window_duration=10,
                                            window_start=0,
                                            number_of_steps=200,
                                            animated=True)

    def run(self):
        
        try:
            ## create commands: 
            cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
            cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
            ## join two commands: 
            cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)

            # ## start a tcp connection
            self.tcp_connection.establish_conn()

            ## we only have two threads: 1 main and the other one for tcpip
            self.tcp_thread = threading.Thread(target=self.tcp_connection.send_receive_thread , args=(self.doorbell_obj,))
            self.tcp_thread.daemon = True
            self.tcp_thread.start()

            
            self.my_oscilloscope.set_active_channel(rs.RIGOL_CHANNEL_IDX.CH4)
            last_cmd_preamble = False
            
            preamble_ch_iterable = self.my_oscilloscope.get_channels_iterable()

            ## Main loop of the thread
            while(True):
                time.sleep(0.1)
                if(self.pause_tcp_connection):                    
                    while(self.doorbell_obj.is_data_new()):
                        pass

                    ## The next available channel is requested from the oscilloscope
                    latest_channel = self.my_oscilloscope.get_next_channel()
                    ## Active channel in the oscilloscope is changed osc model is not thread safe
                    self.my_oscilloscope.set_active_channel(latest_channel)
                    
                    if(True): 
                        ## set to send preamble code each 7 instrcts 
                        self.command_counter += 1
                       
                        cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(latest_channel)
                        cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
                        cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope) 
                        self.doorbell_obj.put_data_to_doorbell(cmd_initiate_oscilloscope) 
                        
                    ## send a request for preamble every 5 instructions, so as not to 
                    ## obstruct data acquisition                    
                    if(self.command_counter > 3): 

                        self.command_counter = 0 
                        next_ch_preamb_request = preamble_ch_iterable.next()
                        cmd_ask_preamble = self.rigol_commander.ask_for_preamble(next_ch_preamb_request)
                        self.doorbell_obj.put_data_to_doorbell(cmd_ask_preamble)
                    

                    ## Check the response of the oscilloscope
                    last_tcp_data:rs.cmdObj = self.tcp_connection.get_data()

                    if(last_tcp_data != None):                         
                        ## get response type
                        response_type = last_tcp_data.get_parser().get_response_type()
                        
                        if(response_type == rs.SCPI_RESPONSE_TYPE.DATA_PAIR):                            
                            last_tcp_data.get_parser().set_x_scale_factor(self.my_oscilloscope.get_x_increment())
                            y_sc_fact = self.my_oscilloscope.get_channel_y_increment(last_tcp_data.get_active_channel())
                            y_offset = self.my_oscilloscope.get_channel_y_offset(last_tcp_data.get_active_channel())
                            x_orig = self.my_oscilloscope.get_x_orig()
                            
                            last_tcp_data.get_parser().set_y_scale_factor(y_sc_fact)
                            last_tcp_data.get_parser().set_x_origin(x_orig)
                            last_tcp_data.get_parser().set_y_offset(y_offset)
                            self.tcp_resp_data_queue.put(last_tcp_data)

                            
                            
                        elif(response_type == rs.SCPI_RESPONSE_TYPE.PREAMBLE):
                            self.my_oscilloscope.update_preamble(last_tcp_data)

                    ## call make thread of the processor
                    self.data_processor.makeThread_RawDataReader()

                    ## get output queue of the prcoessor model
                    output_q = self.data_processor.getOutputQueue()
                    
                    
                    if(not output_q.empty()): 
                    # while(not output_q.empty()): 
                        try: 
                            current_job:controlAndProcess.MathProcess = output_q.get_nowait()
                            if(current_job.is_process_alive()): 
                                output_q.put(current_job)
                            else: 
                                print("con thread {}".format(current_job.get_response()))
                        except: 
                            pass 
                    dbg.flags.cond_print(self.tcp_resp_queue.qsize())
       
        except:
            self.tcp_connection.close_conn() 
            raise 

        finally: 
            self.tcp_connection.close_conn()

    def get_data(self): 
        return self.tcp_connection.get_last_data()

    def get_tcp_data(self):   
        pass 
        ## comment to test processor
        # if(not self.tcp_resp_data_queue.empty()): 
        #     data = self.tcp_resp_data_queue.get_nowait()
        #     return data
        # else: 
        #     return None

    def get_tcp_preamble(self): 
        if(not self.tcp_preamble_queue.empty()): 
            preamble = self.tcp_preamble_queue.get_nowait()
            return preamble
        else: 
            return None        

    
    def get_oscilloscope_instance(self): 
        """
            returns the instance of the oscilloscope class
        """
        return self.my_oscilloscope

    def pause_tcp_connection(self): 
        self.__pause_tcp_conn = True

    def resume_tcp_connection(self): 
        self.__pause_tcp_conn = False

    def finalize_console(self):
        self.tcp_connection.close_conn()