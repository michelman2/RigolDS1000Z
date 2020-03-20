import abc
import queue
import threading

class IQueueSiftableObject(abc.ABC): 

    @abc.abstractmethod
    def get_sifting_parameter(self): 
        pass 
       


class QueueSifter:
    def __init__(self , input_queue:queue.Queue, 
                        sifting_categories:list): 
        """ 
            input_queue: The queue to be sifted based on a parameter
            sifting_categories: A list of parameters based on which input queue
                                is sifted
        """ 
        self.__input_queue = input_queue
        self.__sifting_categories = sifting_categories
        self.__main_thread = None

        if(not isinstance(sifting_categories , list)): 
            raise SiftCatNotList

        if(len(sifting_categories) == 0): 
            raise SiftCatEmpty

        self.__output_queue_cnt = len(sifting_categories)
        
        self.__output_queue_list = [queue.Queue() for _ in range(self.__output_queue_cnt)]

    def sift(self): 
        if(self.__main_thread == None):
            # self.__main_thread = threading.Thread(target=self.__thread_func)
            self.__main_thread = threading.Thread(target=self.__thread_func)
            self.__main_thread.daemon = True
            self.__main_thread.start()

        elif(self.__main_thread.is_alive()): 
            return 
        
        else: 
            # self.__main_thread = threading.Thread(target=self.__thread_func)
            self.__main_thread = threading.Thread(target=self.__thread_func)
            self.__main_thread.daemon = True
            self.__main_thread.start()

    def __cat_to_index(self , category): 
        """
            Returns the index of category in the self.__sifting_categories
        """
        if(not category in self.__sifting_categories):
            raise SiftCatNotFound

        return self.__sifting_categories.index(category)

    
    def __thread_func(self): 
        try: 
            input_token:IQueueForkableObject = self.__input_queue.get_nowait()
            
            cat_index = self.__cat_to_index(input_token.get_sifting_parameter())
            self.__output_queue_list[cat_index].put(input_token)
            

        except: 
            pass
            # raise

    def get_out_queue_list(self): 
        return self.__output_queue_list

    def get_fork_categories(self): 
        return self.__sifting_categories



class InvalidInputArg(Exception): 
    pass

class SiftCatNotFound(Exception): 
    pass

class SiftCatNotList(Exception): 
    pass 

class SiftCatEmpty(Exception): 
    pass


class sifted_obj(IQueueSiftableObject): 

    def __init__(self , id): 
        self.id = id


    def get_sifting_parameter(self): 
        return self.id

    

# import random
# import numpy as np

# myq = queue.Queue()
# sifting_char = [0,1,2,3]
# for i in range(10): 
#     idx = random.randint(np.min(sifting_char),np.max(sifting_char))
#     new_sifted_obj = sifted_obj(idx)
#     myq.put(new_sifted_obj)

# sifter = QueueSifter(input_queue=myq, 
#                     sifting_categories=sifting_char)

# # for i in range(10): 
# #     sifter.sift()

# import time 
# while(not myq.empty()):
#     sifter.sift()
    
    
# output_queues = sifter.get_out_queue_list()

# for currq in output_queues: 
#     print("---")
#     while(not currq.empty()): 
#         object_curr:sifted_obj = currq.get()
#         print(object_curr.get_sifting_parameter())