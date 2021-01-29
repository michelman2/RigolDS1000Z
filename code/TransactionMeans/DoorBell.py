import threading
import typing
from TransactionMeans import LimitedQueue
from TransactionMeans import MessageCarrier 


class DoorBell: 
    ### doorbell object is used to share messages between threads 
    ### One thread in the put data and pick data methods
    data_lock = threading.Lock()
    data = None
    data_new = False 
    
    lim_q:LimitedQueue.LimitedQueue = LimitedQueue.LimitedQueue(10)

    def __init__(self): 
        pass


    def is_data_new(self):
        return not self.lim_q.empty()

        # return self.data_new

    def put_data_to_doorbell(self , use_data):
        self.lim_q.put(use_data) 

        # with self.data_lock: 
        #     self.data = use_data
        #     self.data_new = True
            



    def pick_data_from_doorbell(self)->MessageCarrier.IterMessageList: 
        try: 
            return self.lim_q.get_nowait()
        except: 
            return None

        # with self.data_lock: 
        #     data_copy = self.data
        #     self.data = None
        #     self.data_new = False
        # return data_copy
