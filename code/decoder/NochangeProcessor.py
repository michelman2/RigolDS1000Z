
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



class NoChangeProcessor(controlAndProcess.MathProcess , QueueUtil.IQueueSiftableObject): 
    
    def __init__(self , input_token , threaded=True , kwargs_dict={}): 
        """
            This is meant to be a forwarding processor, no actual 
            processing is done, just raw data is passed  
        """
        super().__init__(input_token , threaded)
       
        self._input_copy_queue = queue.Queue()
        


    def get_response(self): 
        ## in order to get a finished response, 
        ## first the method is_process_alive from super class must be called
        return self._input_copy_queue

    def run_math_process(self): 
        input_token:rs.cmdObj = self.input_token
          

        self._input_copy_queue.put(input_token)
        
    def get_sifting_parameter(self): 
        input_token:rs.cmdObj = self.input_token
        return input_token.get_active_channel()

class NecessaryArgNotPresent(Exception): 
    pass 