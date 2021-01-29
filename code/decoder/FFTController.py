
import FFT
import queue 
import numpy as np
import time
import Rigol_Lib.RigolSCPI as rs
from TransactionMeans import MessageCarrier as mi
import threading
from Gui import controlAndProcess
from TransactionMeans import QueueUtil
import logging

main_logger = logging.getLogger("main_logger")



class FFTController(controlAndProcess.MathProcess , QueueUtil.IQueueSiftableObject): 
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
        self.__fft_calculator = FFT.FFT()


    def get_response(self): 
        ## in order to get a finished response, 
        ## first the method is_process_alive from super class must be called
        return self.__fft_frames_queue

    def run_math_process(self): 
        input_token:rs.cmdObj = self.input_token
        x = input_token.get_parser().get_data_x()
        y = input_token.get_parser().get_data_y()        

        if(self.__window_duration > np.max(x)): 
            self.__window_duration = 0.01 * np.max(x)
            # main_logger.warning("changed fourier window duration to {}".format(self.__window_duration))

        for i in np.linspace(0 , np.max(x) - self.__window_duration , num=self.__number_of_steps): 

            current_start = self.__window_start + i

            # main_logger.info("current start {}".format(current_start))
            # main_logger.info("current channel {}".format(input_token.get_active_channel()))
            try: 
            
                fft_output = self.__fft_calculator.get_fft((x,y), self.__window_duration,current_start)
                fft_tuple = fft_output[0]
                time_window_tuple = fft_output[1]
                cloned_input = input_token.clone_to_cmdParseClone(new_x=fft_tuple[0] ,new_y=fft_tuple[1],added_info={"time_window_tuple":time_window_tuple})
            
            except Exception as e:
                # main_logger.error("{}".format(e))
                raise 
            
            
            self.__fft_frames_queue.put(cloned_input)
        
    def get_sifting_parameter(self): 
        input_token:rs.cmdObj = self.input_token
        return input_token.get_active_channel()

class NecessaryArgNotPresent(Exception): 
    pass 