import socket 
import threading
import enum
import MessageIterables as mes_iter
import time 
from inspect import getframeinfo , currentframe



class TCPcomm(threading.Thread):    

    TIME_OUT = 0.00
  
    def __init__(self): 
        self.__buffer_size = 250000
        self.__ip = '169.254.16.78'
        self.__port = 5555
        self.__data_ready_list = []
        self.__data_lock = threading.Lock()
        self.__port_listener_list = []
        

    def read_buffer(self): 
        ## This function is used regularly in a thread to read the receive buffer of 
        #   the TCP port.         
        while(True): 
            try:     
                # print("in read_buffer")       
                with self.__data_lock: 
                    data = self.__s.recv(self.__buffer_size)
                    # print("after receive buffer")
                    self.__data_ready_list.append(data)
                    # print("after append data list")


        ### CAREFUL! 
        ### putting inform listeners will make a lock loop, in which the program will stop 

                self.inform_listeners()

            except:              
                pass 


            
    def send_mesage(self , message_object): 
        ## sending message is not put in a thread, it is done in the main thread
        ## but receiving a response and checking the buffer is done in a separate thread 
        #  from the run(self) funtion
        
        try: 
            while(message_object.has_next()):            
                current_message = message_object.next().get_cmd()
                self.__s.send(current_message.encode())        
        except: 
            # pass
            raise 

    ## Implementation of observer pattern
    def subscribe_listener(self , listener): 
        ## A listener is an object that implements an inform() method
        ## and can reuest subscription to the tcp comm object
        with self.__data_lock: 
            self.__port_listener_list.append(listener)

    def inform_listeners(self): 
        ## in this function, the listener objects that have subscribed to the tcp comm object, 
        #  are informed that a new data is put in the list
        
        for listener in self.__port_listener_list: 
            listener.inform()
    
    def get_all_messages(self): 
        ## The listener has to call this function to get all of the received messages, 
        #  This function is threadsafe
        with self.__data_lock: 
            data = self.__data_ready_list
            self.__data_ready_list = []
        
        return data


    def establish_conn(self): 
        try: 
            self.__s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.__s.setblocking(1)           
            self.__s.connect((self.__ip , self.__port))
            self.__s.settimeout(self.TIME_OUT)
        except: 
            self.__s.close()
            raise 

    def close_conn(self): 
        self.__s.close()
        
    def set_ip(self , ip):
        self.__ip = ip

    def set_port(self , port): 
        self.__port = port

    def set_buffer_size(self , buffer_size): 
        self.__buffer_size = buffer_size

    def set_message(self , message):
        if(not isinstance(message , mes_iter.MessageIterable)): 
            raise TypeError


         
        