
import FFTModule
import queue 
import numpy as np
import time
import Rigol_Lib.RigolSCPI as rs
from TCPconnection import MessageIterables as mi
import threading

class FFTController: 



    def __init__(self, data_tuple, 
                        window_duration, 
                        window_start_time,
                        animated = False):

        self.data_tuple = data_tuple
        self.window_duration = window_duration
        self.window_start_time = window_start_time
        self.operation_done = False 
        self.fft_calculator = FFTModule.FFTModule()
        self.animated = animated
        self.frame_queue = queue.Queue() 
        self.frame_list = []


    def run(self):
       
        while(not self.operation_done): 
            time.sleep(0.1)
            # print("############### {}".format(self.data_tuple!=None))
            if(self.data_tuple != None and self.operation_done == False):  
               
                if(self.animated == True): 
                    
                    for i in np.arange(0 , np.max(self.data_tuple[0]) - self.window_duration , step =0.1): 

                        current_start = self.window_start_time + i

                        [fft_tuple , time_window_tuple] = self.fft_calculator.get_fft(self.data_tuple, 
                                                                                    self.window_duration,
                                                                                    current_start)
                    
                        # self.frame_queue.put([fft_tuple , time_window_tuple])
                        self.frame_list.append([fft_tuple , time_window_tuple])

                else: 
                    [fft_tuple , time_window_tuple] = self.fft_calculator.get_fft(self.data_tuple, 
                                                                                    self.window_duration,
                                                                                    self.window_start_time)

                    # self.frame_queue.put([fft_tuple , time_window_tuple])
                    self.frame_list.append([fft_tuple , time_window_tuple])

                self.operation_done = True

            # if(self.operation_done): 
            #     print("////////////////////////////// done fft {}".format(len(self.frame_list)))

    # def set_oscill_data_tuple(self , data_tuple): 
    #     self.data_tuple = data_tuple
    #     self.frame_queue.queue.clear()

    def is_operation_done(self): 
        return self.operation_done

    def get_queue(self):
        return self.frame_queue

    def get_frame_list(self):
        # print("-------- frame list ----- got frame list---- {}".format(len(self.frame_list))) 
        return self.frame_list


class FFTControllerOscillAdapter: 
    
    
    oscill_cmd_object:rs.cmdObj = None
    data_tuple = None
    fft_controller = None 
    fourier_thread = None
    resulting_frame_is_returned = False

    def __init__(self,oscill_cmd_obj, 
                    window_duration, 
                    window_start_time,
                    animated = False):

        self.oscill_cmd_object = oscill_cmd_obj
        x = self.oscill_cmd_object.get_parser().get_data_idx()
        y = self.oscill_cmd_object.get_parser().get_data_val()
        self.data_tuple = (x , y)

        self.fft_controller = FFTController(self.data_tuple,
                                            window_duration=window_duration,
                                            window_start_time=window_start_time, 
                                            animated=animated)
        
        self.fourier_thread = threading.Thread(target=self.run)
        self.fourier_thread.daemon = True 

    # def __del__(self): 
    #     # print("**************************** ffft stopped")
    #     self.fourier_thread._stop()
     
    def stop_thread(self): 
        self.fourier_thread._stop()

    def get_command_object(self)->rs.cmdObj: 
        return self.oscill_cmd_object
    
    def start_calc_thread(self): 
        self.fourier_thread.start()
        

    def run(self): 
        self.fft_controller.run()


    def is_operation_done(self): 
        return self.fft_controller.is_operation_done()

    def get_iterable_frames(self)->mi.IterMessageList:
        if(self.resulting_frame_is_returned): 
            return None 

        if(self.is_operation_done() and self.fft_controller.get_frame_list()):
            self.resulting_frame_is_returned = True
            return mi.IterMessageList(self.fft_controller.get_frame_list()) 
        else: 
            return None 