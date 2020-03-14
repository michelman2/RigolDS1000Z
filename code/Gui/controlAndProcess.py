from Gui import console_thread
from Rigol_Lib import RigolSCPI
from TransactionMeans import LimitedQueue
import threading
import queue
import abc

class MathProcess(abc.ABC):
    
    def __init__(self , input_token , threaded=True):
        if(threaded): 
            ## The input token can be of any form (raw token, cmdObj) 
            self.input_token = input_token
            self.__objects_thread = threading.Thread(target=self.run_math_process)
            self.__objects_thread.daemon = True

    def start_process(self): 
        self.__objects_thread.start()

    def is_process_alive(self): 
        return self.__objects_thread.is_alive()   

    def get_input_token(self): 
        return self.input_token

    @abc.abstractclassmethod
    def run_math_process(self): 
        """
            Runs the math process to function on data 
        """
        # self.__resp = self.__input_token * 2
        pass 

class fftprocess(MathProcess): 
    def __init__(self , input_token , threaded=True): 
        super(fftprocess , self).__init__(input_token , threaded)

    def run_math_process(self): 
        self.__response = self.input_token * 2

    def get_response(self): 
        return self.__response 

class ProcessModel: 

    def __init__(self): 
        self.__running_processes_queue:LimitedQueue.LimitedQueue = LimitedQueue.LimitedQueue(10)
        self.__rawDataReader_thread_ = None 
        self.__connect_func_queue_pair = {}
        ## output pipe queue 
        self.__output_processes_queue:queue.Queue = queue.Queue()
        self.__math_processor:MathProcess = None 

        self.__log_list = []




    def setProcessor(self, math_processor:MathProcess): 
        """ 
            Sets the type of the mathematical processor that is used
            for data
        """
        self.__math_processor = math_processor
        


    def makeThread_RawDataReader(self): 
        """
            Launches only one thread for getting data from 
            an input queue
        """
        if(self.__rawDataReader_thread_ == None): 
            self.__rawDataReader_thread_ = threading.Thread(target=self.rawDataRead)
            self.__rawDataReader_thread_.daemon = True
            self.__rawDataReader_thread_.start()

        elif(not self.__rawDataReader_thread_.is_alive()): 
            self.__rawDataReader_thread_ = None 
            


    def rawDataRead(self):
        """
            Reads data from a connected queue, the queue has to be connected 
            before the function is called
        """

        ## The functions name is used as index in when connecting a function to 
        ## it's queue 
        current_function_ptr = self.rawDataRead
        try:
            ## The queue contains objects to be read
            connected_q:LimitedQueue.LimitedQueue = self.__connect_func_queue_pair[current_function_ptr]
            
            ## Getting data from queue
            while(not connected_q.empty()): 
                try:
                    if(self.__math_processor == None): 
                        raise MissingMathProcessor

                    ## Get one token from input 
                    raw_data_token = connected_q.get_nowait()
                    self.__log_list.append(raw_data_token)
                    ## Launch a process with the input token
                    math_proc = self.__math_processor(raw_data_token)
                    math_proc.start_process()
                    ## put the token into output queue
                    self.__output_processes_queue.put(math_proc)

                except: 
                    pass 
        except: 
            raise

    def getLogData(self): 
        """
            Returns log data for later printing  
        """
        return self.__log_list

    def connect_f2q(self , func_ref_in_obj=None , queue_to_be_read=None):
        """
            Connecting a function to a queue
            The function is used to get queue contents, implementation 
            of observer pattern in multithreaded application using message 
            queues.
            The connection has to be made by the owner of the object
        """
        if(queue_to_be_read == None or func_ref_in_obj == None): 
            raise MissingLinkInConnection
        else:
            self.__connect_func_queue_pair[func_ref_in_obj] = queue_to_be_read

    def getOutputQueue(self):
        """
            returns the output queue, the process that are 
            already done are put in this queue 
        """ 
        return self.__output_processes_queue
    

class MissingMathProcessor(Exception): 
    pass
class MissingLinkInConnection(Exception): 
    pass