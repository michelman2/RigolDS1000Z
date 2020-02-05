import threading

class TCPListener: 
    __data_in_main_thread = []
    # __tcp_listener_lock = threading.Lock()

    def __init__(self , tcp_source): 
        self.__tcp_obj = tcp_source
        self.__tcp_obj.subscribe_listener(self)


    def inform(self): 
        ## The application to read data has to be thread safe
        # with self.__tcp_listener_lock: 
        data_list = self.__tcp_obj.get_all_messages()
        
        for data in data_list: 
            self.__data_in_main_thread.append(data)


    def get_first_in_queue(self): 
        # with self.__tcp_listener_lock: 
        if(len(self.__data_in_main_thread) == 0):
            return None
        else: 
            current_data = self.__data_in_main_thread[0]
            self.__data_in_main_thread.remove(current_data)
            return current_data 
