import threading

class TCPListener: 
    __data_in_main_thread = []
    __tcp_listener_lock = threading.Lock()
    __last_data = None
    __current_idx = 0

    def __init__(self , tcp_source): 
        self.__tcp_obj = tcp_source
        self.__tcp_obj.subscribe_listener(self)


    def inform(self): 
        ## The application to read data has to be thread safe
        with self.__tcp_listener_lock: 
            data_list = self.__tcp_obj.get_all_messages()
            
            for data in data_list:
                print(data)
                # data_to_list_type = list(data)
                # if(data_to_list_type[-1] == 10): 
                self.__data_in_main_thread.append(data)
                self.__data_in_main_thread.insert(self.__current_idx, data)
                self.__current_idx += 1 
                if(self.__current_idx >= 5): 
                    self.__current_idx = 0 
                # queued_data_len = len(self.__data_in_main_thread)
                # if( queued_data_len >=5): 
                #     for remove_cnt in range(0, queued_data_len - 5): 
                #         self.__data_in_main_thread.remove(0)
                

    def inform_last(self): 
        with self.__tcp_listener_lock: 
            data_list = self.__tcp_obj.get_all_messages()
            if(len(data_list) > 0 ): 
                self.__last_data = data_list[0]
          


    def get_first_in_queue(self): 
        # print("inside get_first_in_queue")
        with self.__tcp_listener_lock: 
            if(len(self.__data_in_main_thread) == 0):
                return None
            else: 
                current_data = self.__data_in_main_thread[0]
                # self.__data_in_main_thread.remove(current_data)
                return current_data 


