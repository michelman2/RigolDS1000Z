import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import threading

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

class ConsoleControl: 
    """ 
        A wrapper class to put the console application and its functionality 
        in a single object. This class launches threads to handle tcp connection. 

        Can be used as the main thread when using none-gui applications
        Can be launched in a second thread (the run method) when using gui applications

    """
    
    global doorbell_obj # doorbell objet is used between the thread running this class and the thread handling tcp connections

    queue_max_size = 10
    # tcp_resp_queue = queue.Queue()
    tcp_resp_queue = LimitedQueue.LimitedQueue(queue_max_size)
    fft_resp_queue = LimitedQueue.LimitedQueue(queue_max_size)

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

    def run(self):
        
        try:
            
            ## create commands: 
            cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
            cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
            ## join two commands: 
            cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)

            ## start a tcp connection
            self.tcp_connection.establish_conn()

            ## we only have two threads: 1 main and the other one for tcpip
            self.tcp_thread = threading.Thread(target=self.tcp_connection.send_receive_thread , args=(self.doorbell_obj,))
            self.tcp_thread.daemon = True
            self.tcp_thread.start()

            latest_channel = rs.RIGOL_CHANNEL_IDX.CH4
            while(True):
                if(self.pause_tcp_connection):                    
                    while(self.doorbell_obj.is_data_new()):
                        pass

                    ## just to generate channel commands for the 
                    ## osciolloscope
                    if(latest_channel == rs.RIGOL_CHANNEL_IDX.CH3):  
                        latest_channel = rs.RIGOL_CHANNEL_IDX.CH4

                    elif(latest_channel == rs.RIGOL_CHANNEL_IDX.CH4): 
                        latest_channel = rs.RIGOL_CHANNEL_IDX.CH3
                        

                    cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(latest_channel)
                    cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
                    cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)
                    
                    self.doorbell_obj.put_data_to_doorbell(cmd_initiate_oscilloscope)   ## put date to doorbell
                    
                    ## last data
                    last_tcp_data:rs.cmdObj = self.tcp_connection.get_data()
                    if(last_tcp_data != None): 
                        
                        
                        self.tcp_resp_queue.put(last_tcp_data)
                        
                        ########### extract tcp data here: instead of gui
                        response_type = last_tcp_data.get_parser().get_response_type()
                        
                        if(response_type == rs.SCPI_RESPONSE_TYPE.DATA_PAIR):
                            
                            self.tcp_resp_data_queue.put(last_tcp_data)
                            # print("************* data type {}".format(last_tcp_data.get_active_channel()))


                        
                    
                    dbg.flags.cond_print(self.tcp_resp_queue.qsize())
                    

        

        except:
            self.tcp_connection.close_conn() 
            raise 

        finally: 
            self.tcp_connection.close_conn()

    def get_data(self): 
        return self.tcp_connection.get_last_data()

    def get_tcp_data(self):   
        if(not self.tcp_resp_queue.empty()): 
            # data = self.tcp_resp_queue.get()
            data = self.tcp_resp_data_queue.get_nowait()
            return data
        else: 
            return None
        

    def pause_tcp_connection(self): 
        self.__pause_tcp_conn = True

    def resume_tcp_connection(self): 
        self.__pause_tcp_conn = False

    def finalize_console(self):
        self.tcp_connection.close_conn()