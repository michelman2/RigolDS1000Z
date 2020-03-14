import abc
import typing
import queue
import threading

class Offloader(abc.ABC): 

    def __init__(self): 
        ## for each process a queue entry is created 
        self.__processor_list = []
        # self.__offload_queue:queue.Queue = [] 
        self.__response_q_list:list = [] 
    
    
    
    def launchProcess(self, processor:Processor , process_input): 
        """
            calls the input queue of the processor
        """
        response_queue = queue.Queue()
        self.__response_q_list.append(response_queue)
        # process = Processor(process_input , response_queue)
        self.__processor_list.append(processor)
        processor.start_thread()
    

    


class Processor(abc.ABC): 
    def __init__(self , process_input , response_queue):         
        self.__response_queue = response_queue
        self.__process_input = process_input
        self.__process_id = 0

        self.p_thread = threading.Thread(target=self.run)
        self.p_thread.daemon = True

    
    @abc.abstractclassmethod
    def run(self): 
        """
            the main process goes into here, 
            The object finishes running after  
        """
        pass
    
    
    def setProcessId(self , id): 
        self.__process_id = id

    def getProcessId(self):
        return self.__process_id

    def start_thread(self): 
        self.p_thread.start()
    
        

class fftcontroller(Offloader):
    def __init__(self): 
        super()

    def test(self): 
        for i in range(10): 
            pass 

        

class fftcaclculator(Processor): 
    def __init__(self , p_input , resp_queue): 
        super(p_input , resp_queue)



    def run(self):
        output = 2 * self.__process_input
        self.__response_queue.put(output) 

    
    