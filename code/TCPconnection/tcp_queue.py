import numpy as np
import threading 
from threading import Lock


class tcp_queue: 

    queue_lock = Lock() 
    queue = None

    def __init__(self, queue_space_limit = 0):
        self.queue_space_limit = queue_space_limit 
        self.queue = []
        


    def put(self , item):         
        with self.queue_lock: 
            self.queue.append(item)
            if(self.qsize() > self.queue_space_limit):
                self.remove_oldest()


    def get(self): 
        with self.queue_lock: 
            if(self.qsize() > 0):
                return self.queue.pop(self.qsize()-1)
            else: 
                return None 
    
    def remove_oldest(self):
        with self.queue_lock: 
            if(not self.empty()): 
                self.queue.remove(self.queue[0]) 

    def qsize(self): 
        print("lock1")
        with self.queue_lock:
            print("lock2") 
            return len(self.queue) 


    def empty(self): 
        with self.queue_lock:
            print("locked") 
            if(self.qsize() > 0): 
                print("release")
                return True
            else:
                print("release") 
                return False
            

    def clear(self): 
        with self.queue_lock: 
            self.queue = []

    
    class __inner_queue: 
        def __init__(self):
            pass 

        def clear(self): 
            pass 