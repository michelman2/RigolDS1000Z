import abc 
import threading
import queue
from Rigol_Lib import RigolSCPI as rs
import time
from Gui import controlAndProcess
from TransactionMeans import LimitedQueue
import sys

import logging 
import pickle 
main_logger = logging.getLogger("main_logger")

class IbundlePlotToGui(abc.ABC): 
    def __init__(self, id ,  threaded=True): 
        """
            Abstract class working as an interface to model painting data on
            canvas 
        """
        self.__function_to_q_dict = {}
        self.canvas_ref = None 
        self.__id = id 

        if(threaded):
            self.paint_thread = threading.Thread(target=self.set_canvas_data)
            self.paint_thread.daemon = True 
    
    
    def setCanvas(self , canvas_reference): 
        """ 
            Gets the type of canvas that it needs to paint on 
        """
        if(isinstance(canvas_reference , list)): 
            pass 
        else: 
            canvas_reference = [canvas_reference]

        self.canvas_ref = canvas_reference 


    def connect_input_q(self , queue_reference): 
        """
            connectes input data pipe (queue) to a function
            in this object that is responsible for data collection 
        """
        ## only one queue is handled by this class 
        self.input_q = queue_reference

    def isProcessAlive(self): 
        return self.paint_thread.is_alive()

    
    def startBundling(self): 
        if(self.canvas_ref == None): 
            raise NoCanvasSet    
        
        
        if(self.paint_thread.is_alive()): 
            ## returns if previous thread is not done yet
            return 

        
        self.paint_thread = threading.Thread(target=self.set_canvas_data)
        self.paint_thread.daemon = True
        self.paint_thread.start()
         
    def id(self): 
        return self.__id

    @abc.abstractmethod
    def set_canvas_data(self): 
        """ 
            Runs an operation in the main thread of the object
        """
        pass 

    
    


class IbundleSyncPlotsToGui(IbundlePlotToGui):
    def __init__(self ,id ,  threaded= True): 
        super().__init__(id , threaded=threaded)
        self.data_expander = None 

    
    def set_data_expander(self , data_expander): 
        """
            data_multiplier tries to extract data from a single input token
        """
        self.data_expander = data_expander

    def startBundling(self): 
        if(self.data_expander == None):
            raise DMultiplierNotSet

        super().startBundling()

    @abc.abstractmethod
    def set_canvas_data(self): 
        pass



class bundleFFTtoCanvas(IbundleSyncPlotsToGui): 
    def __init__(self, id , threaded = True): 
        super().__init__(id , threaded=threaded)
        

    def set_canvas_data(self): 
        
        in_queue:queue.Queue = self.input_q

        try: 
            token:controlAndProcess.MathProcess = in_queue.get_nowait()
            frame_group:queue.Queue = token.get_response()
            
            while(not frame_group.empty()):
                frame:rs.cmdObj = frame_group.get() 
                try:
                    cmd_history = self.data_expander.expand_data(frame)
                    cmd_len = len(cmd_history)
                    
                    for idx , canvas in enumerate(self.canvas_ref):
                        
                        current_frame = cmd_history[cmd_len - 1 - idx]                    
                        
                        data_x = current_frame.get_parser().get_data_x()
                        data_y = current_frame.get_parser().get_data_y()
                        
                        
                        canvas.setData(data_x , data_y)

                        

                except: 
                    
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print(exc_value)
                    raise

                time.sleep(0.05)
            
        except:
            # raise 
            pass  

class bundleNoChangeToCanvas(IbundleSyncPlotsToGui): 
    previous_time = 0 

    def __init__(self, id , threaded = True): 
        super().__init__(id , threaded=threaded)
        

    def set_canvas_data(self): 
        
        in_queue:queue.Queue = self.input_q

        try: 
            token:controlAndProcess.MathProcess = in_queue.get_nowait()
            frame_group:queue.Queue = token.get_response()
            
            while(not frame_group.empty()):
                frame:rs.cmdObj = frame_group.get() 
                try:
                    cmd_history = [frame]
                    # cmd_history = self.data_expander.expand_data(frame)
                    cmd_len = len(cmd_history)
                    
                    for idx , canvas in enumerate(self.canvas_ref):
                        
                        current_frame = cmd_history[0]                    
                        
                        data_x = current_frame.get_parser().get_data_x()
                        data_y = current_frame.get_parser().get_data_y()
                        
                        current_time = time.time() 
                        if(current_time - bundleNoChangeToCanvas.previous_time > 1): 
                            bundleNoChangeToCanvas.previous_time = current_time
                            data_dict = {"x":data_x , "y":data_y , "srate":5000000}
                            base_addr = "D:/Academic/My projects/3.LuxLink+/CommLink/Initial results/sampling/shutter_3x/"
                            name = str(int(time.time())) + "_low_freq_pulse_3_shutters,{}".format(current_frame.get_active_channel()) + ".pickle"
                            full_addr = base_addr + name
                            pickle_out = open(full_addr,"wb")
                            pickle.dump(data_dict, pickle_out)
                            pickle_out.close() 
                        canvas.setData(data_x , data_y)

                        

                except: 
                    
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print(exc_value)
                    raise

                time.sleep(0.05)
            
        except:
            # raise 
            pass  



class NoCanvasSet(Exception): 
    pass


class ArgTypeErro(Exception): 
    pass

class ArgCountError(Exception): 
    pass


class DMultiplierNotSet(Exception): 
    pass