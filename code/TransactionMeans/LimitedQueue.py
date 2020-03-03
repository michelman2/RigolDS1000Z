import numpy 
import queue


class LimitedQueue: 


    def __init__(self , max_queue_size): 
        self.__max_queue_size = max_queue_size
        self.__queue = queue.Queue()
        
    
    def put(self, item):
        self.__queue.put(item)
        if(self.__queue.qsize() > self.__max_queue_size): 
            self.__queue.get()

    
    def get(self): 
        return self.__queue.get()

    
    def qsize(self): 
        return self.__queue.qsize()


    def empty(self): 
        return self.__queue.empty()
    
    def get_nowait(self): 
        return self.__queue.get_nowait()