
import FFTModule
import queue 
import numpy as np
import time
import Rigol_Lib.RigolSCPI as rs
from TCPconnection import MessageIterables as mi
import threading
from Gui import controlAndProcess
from TransactionMeans import QueueUtil


# class FFTController:
#     def __init__(self, data_tuple, 
#                         window_duration, 
#                         window_start_time,
#                         number_of_steps,
#                         animated = False):

#         self.data_tuple = data_tuple
#         self.number_of_steps = number_of_steps
#         self.window_duration = window_duration
#         self.window_start_time = window_start_time
#         self.operation_done = False 
#         self.fft_calculator = FFTModule.FFTModule()
#         self.animated = animated
#         self.frame_queue = queue.Queue() 
#         self.frame_list = []


#     def run(self):
#         while(not self.operation_done): 
#             time.sleep(0.1)
#             # print("############### {}".format(self.data_tuple!=None))
#             if(self.data_tuple != None and self.operation_done == False):  
               
#                 if(self.animated == True): 
                    
#                     for i in np.linspace(0 , np.max(self.data_tuple[0]) - self.window_duration , num=self.number_of_steps): 

#                         current_start = self.window_start_time + i

#                         [fft_tuple , time_window_tuple] = self.fft_calculator.get_fft(self.data_tuple, 
#                                                                                     self.window_duration,
#                                                                                     current_start)
                    
                        
#                         self.frame_list.append([fft_tuple , time_window_tuple])

#                 else: 
#                     [fft_tuple , time_window_tuple] = self.fft_calculator.get_fft(self.data_tuple, 
#                                                                                     self.window_duration,
#                                                                                     self.window_start_time)

                   
#                     self.frame_list.append([fft_tuple , time_window_tuple])

#                 self.operation_done = True

            

#     def is_operation_done(self): 
#         return self.operation_done

#     def get_queue(self):
#         return self.frame_queue

#     def get_frame_list(self):
#         # print("-------- frame list ----- got frame list---- {}".format(len(self.frame_list))) 
#         return self.frame_list


# class FFTControllerOscillAdapter: 
    
    
#     oscill_cmd_object:rs.cmdObj = None
#     data_tuple = None
#     fft_controller = None 
#     fourier_thread = None
#     resulting_frame_is_returned = False

#     def __init__(self,oscill_cmd_obj, 
#                     window_duration, 
#                     window_start_time,
#                     number_of_steps,
#                     animated = False):
        

#         self.oscill_cmd_object = oscill_cmd_obj
        
#         x = self.oscill_cmd_object.get_parser().get_data_x_idx()
#         y = self.oscill_cmd_object.get_parser().get_data_y_idx()
#         self.data_tuple = (x , y)

#         self.fft_controller = FFTController(self.data_tuple,
#                                             window_duration=window_duration,
#                                             window_start_time=window_start_time,
#                                             number_of_steps=number_of_steps,
#                                             animated=animated)
        
#         self.fourier_thread = threading.Thread(target=self.run)
#         self.fourier_thread.daemon = True 

#     def stop_thread(self): 
#         self.fourier_thread._stop()

#     def get_command_object(self)->rs.cmdObj: 
#         return self.oscill_cmd_object
    
#     def start_calc_thread(self): 
#         self.fourier_thread.start()
        

#     def run(self): 
#         self.fft_controller.run()


#     def is_operation_done(self): 
#         return self.fft_controller.is_operation_done()

#     def get_iterable_frames(self)->mi.IterMessageList:
#         if(self.resulting_frame_is_returned): 
#             return None 

#         if(self.is_operation_done() and self.fft_controller.get_frame_list()):
#             self.resulting_frame_is_returned = True
#             return mi.IterMessageList(self.fft_controller.get_frame_list()) 
#         else: 
#             return None 


class FFTObserver(controlAndProcess.MathProcess , QueueUtil.IQueueSiftableObject): 
    ## additional arguments for fft_observer is: 
    ## window_duration
    ## window_start
    ## number of steps 
    ## animated or single frame fft
    def __init__(self , input_token , threaded=True , kwargs_dict={}): 
        """
            The class implements the math processor abstract class
            the arguments in **kwargs are: 
                window_duration 
                window_start 
                number_of_steps 
                animated (if False means only one single frame of fft is calculated)
        """
        window_duration_text = 'window_duration'
        window_start_text = 'window_start'
        number_of_steps_text = 'number_of_steps'
        animated_text = 'animated'

        if(not window_duration_text in kwargs_dict or 
            not window_start_text in kwargs_dict or 
            not number_of_steps_text in kwargs_dict or 
            not animated_text in kwargs_dict):
            raise NecessaryArgNotPresent
        
        
        
        self.__window_duration = kwargs_dict[window_duration_text]
        self.__window_start = kwargs_dict[window_start_text]
        self.__number_of_steps = kwargs_dict[number_of_steps_text]
        self.__animated = kwargs_dict[animated_text]

        super().__init__(input_token , threaded)
        ## The queue to hold fft responses as a function of their 
        ## start time
        self.__fft_frames_queue = queue.Queue()
        self.__fft_calculator = FFTModule.FFTModule()


    def get_response(self): 
        ## in order to get a finished response, 
        ## first the method is_process_alive from super class must be called
        return self.__fft_frames_queue

    def run_math_process(self): 
        input_token:rs.cmdObj = self.input_token
        x = input_token.get_parser().get_data_x()
        y = input_token.get_parser().get_data_y()        

        for i in np.linspace(0 , np.max(x) - self.__window_duration , num=self.__number_of_steps): 

                        current_start = self.__window_start + i

                        [fft_tuple , time_window_tuple] = self.__fft_calculator.get_fft((x,y), 
                                                                                    self.__window_duration,
                                                                                    current_start)
                    
                        cloned_input = input_token.clone_to_cmdParseClone(new_x=fft_tuple[0] ,
                                                                            new_y=fft_tuple[1],
                                                                            added_info={"time_window_tuple":time_window_tuple})
                        
                        
                        
                        self.__fft_frames_queue.put(cloned_input)
        
    def get_sifting_parameter(self): 
        input_token:rs.cmdObj = self.input_token
        return input_token.get_active_channel()

class NecessaryArgNotPresent(Exception): 
    pass 