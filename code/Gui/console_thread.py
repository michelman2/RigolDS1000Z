import __init__

import threading
import Rigol_Lib.RigolSCPI as rs
import TransactionMeans.MessageCarrier as mi
import TCPconnection.TCPcomm as tcp

from Rigol_util import channelDataKeeper as cld
from Rigol_util import RigolCommander as rc
from TransactionMeans import DoorBell as db 

from decoder import SineCreator
from decoder import NochangeProcessor
import time
import queue
from TransactionMeans import LimitedQueue
from debug import debug_instr as dbg
from Rigol_util import Oscilloscope_model
from Gui import controlAndProcess
from decoder import FFTController
from Gui import bundlePlotToGui
from TransactionMeans import MeaningfulList
from TransactionMeans import QueueUtil as qutil
from Gui import historyExtractor
from Gui import bundleManager
import logging 

main_logger = logging.getLogger("main_logger")

class ConsoleControl: 
    """ 
        A wrapper class to put the console application and its functionality 
        in a single object. This class launches threads to handle tcp connection. 

        Can be used as the main thread when using none-gui applications
        Can be launched in a second thread (the run method) when using gui applications

    """
    
    command_counter = 0 
   
    data_processor = controlAndProcess.MathProcessController()

    ## oscilloscope model holds the state of the oscilloscope at each time
    my_oscilloscope:Oscilloscope_model.Oscilloscope = Oscilloscope_model.Oscilloscope(available_channels=[
                                                                                        rs.RIGOL_CHANNEL_IDX.CH1,                   
                                                                                        rs.RIGOL_CHANNEL_IDX.CH2, 
                                                                                        rs.RIGOL_CHANNEL_IDX.CH3,
                                                                                        rs.RIGOL_CHANNEL_IDX.CH4], 
                                                                                    active_channels=[
                                                                                        rs.RIGOL_CHANNEL_IDX.CH1,
                                                                                        rs.RIGOL_CHANNEL_IDX.CH2,
                                                                                        rs.RIGOL_CHANNEL_IDX.CH3,
                                                                                        rs.RIGOL_CHANNEL_IDX.CH4
                                                                                    ])

    
    queue_max_size = 10
    tcp_preamble_queue = LimitedQueue.LimitedQueue(queue_max_size)
    tcp_resp_data_queue = LimitedQueue.LimitedQueue(queue_max_size)
    ready_math_process_q = LimitedQueue.LimitedQueue(queue_max_size)

    def __init__(self):
        ## create a list to hold all data bundler references
        self.__bundles_to_canvas = MeaningfulList.MeaningfulList(row=self.my_oscilloscope.get_channel_cnt(),
                                                                column=2)

        
        # create doorbell object for message passing between main thread
        # and the single thread
        self.doorbell_obj = db.DoorBell()

        ## create commander object to manage generation of commands
        self.rigol_commander = rc.RigolCommander()

        ## create tcp object: manages send, receive, connection
        self.tcp_connection = tcp.TCPcomm(ip='169.254.16.78' , port=5555)

        self.__pause_tcp_conn = False

        self.data_processor.connect_f2q(self.data_processor.rawDataRead ,
                                        self.tcp_resp_data_queue)
        
        # self.data_processor.setProcessor(FFTController.FFTController,
        #                                     window_duration=10,
        #                                     window_start=0,
        #                                     number_of_steps=200,
        #                                     animated=True)

        self.data_processor.setProcessor(NochangeProcessor.NoChangeProcessor)

        self.data_sifter = qutil.QueueSifter(input_queue=self.ready_math_process_q,
                                                    sifting_categories=self.my_oscilloscope.get_channel_list())
        
        self.channel_sifted_q_list = self.data_sifter.get_out_queue_list()
        
        self.cmdObj_history_extractor = historyExtractor.cmdObjHistoryExctractor(history_depth=1)
    
        
        self._bundler_list = []
        for ch_idx in range(self.my_oscilloscope.get_channel_cnt()): 
            # new_bundle = bundlePlotToGui.bundleFFTtoCanvas(id=ch_idx)
            new_bundle = bundlePlotToGui.bundleNoChangeToCanvas(id=ch_idx)

            new_bundle.set_data_expander(data_expander=self.cmdObj_history_extractor)
            new_bundle.connect_input_q(self.channel_sifted_q_list[ch_idx])
            
            self._bundler_list.append(new_bundle)
            
        
    def get_data_gui_bundlers(self): 
        return self._bundler_list

    def run(self):
        
        try:
            cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
            cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
            cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)

            self.tcp_connection.establish_conn()

            ## we only have two threads: 1 main and the other one for tcpip
            self.tcp_thread = threading.Thread(target=self.tcp_connection.send_receive_thread , args=(self.doorbell_obj,))
            self.tcp_thread.daemon = True
            self.tcp_thread.start()

            
            self.my_oscilloscope.set_active_channel(rs.RIGOL_CHANNEL_IDX.CH4)
            last_cmd_preamble = False
            
            preamble_ch_iterable = self.my_oscilloscope.get_active_channels_iterable()

            ## Main loop of the thread
            while(True):
                time.sleep(0.4)
                # print(self.ready_math_process_q.qsize())
                if(self.pause_tcp_connection):                    
                    while(self.doorbell_obj.is_data_new()):
                        time.sleep(0.1)
                        pass

                    
                    latest_channel = self.my_oscilloscope.get_next_channel()
                    self.my_oscilloscope.set_active_channel(latest_channel)
                    
                    
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
                        # main_logger.info("ch:request: {}".format(next_ch_preamb_request))
                        cmd_ask_preamble = self.rigol_commander.ask_for_preamble(next_ch_preamb_request)
                        self.doorbell_obj.put_data_to_doorbell(cmd_ask_preamble)
                    

                    ## Check the response of the oscilloscope
                    last_tcp_data:rs.cmdObj = self.tcp_connection.get_data()

                    if(last_tcp_data != None):                         
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

                  
                    self.data_processor.makeThread_RawDataReader()

                    ## get output queue of the prcoessor model
                    math_proc_out_q = self.data_processor.getOutputQueue()                    
                    
                    if(not math_proc_out_q.empty()): 
                        try: 
                            current_job:controlAndProcess.MathProcess = math_proc_out_q.get_nowait()
                            if(current_job.is_process_alive()): 
                                math_proc_out_q.put(current_job)
                            else: 
                                self.ready_math_process_q.put(current_job)
                        except: 
                            pass 
                    
                    self.data_sifter.sift()

                    
        except:
            self.tcp_connection.close_conn() 
            raise 

        finally: 
            self.tcp_connection.close_conn()


    def get_data(self): 
        return self.tcp_connection.get_last_data()

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