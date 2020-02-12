import socket 
import threading
import enum
import MessageIterables as mes_iter
import time 
from inspect import getframeinfo , currentframe
import typing
import doorbell.DoorBell as db
import queue

class TCPcomm(threading.Thread):    

    TIME_OUT = 0.00
  
    def __init__(self): 
        self.__buffer_size = 250000
        self.__ip = '169.254.16.78'
        # self.__ip = '169.254.16.79'
        self.__port = 5555
        self.__data_ready_list = []
        self.__data_lock = threading.Lock()
        self.__port_listener_list = []
        self.__recv_data_queue = queue.Queue()

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
                # raise


            
    def send_mesage(self , message_object): 
        ## sending message is not put in a thread, it is done in the main thread
        ## but receiving a response and checking the buffer is done in a separate thread 
        #  from the run(self) funtion
        
        try: 
            while(message_object.has_next()):            
                current_message = message_object.next().get_cmd()
                self.__s.send(current_message.encode())        
        except: 
            # raise
            pass 

    def send_receive_thread(self , doorbell_obj:db.DoorBell):
        ## assume that if data is not null, it should be from message iterable type
        ## wait until data in the doorbell is taken by another thread
        while(True): 
            # this function needs to be put in a separate thread
            while(doorbell_obj.is_data_new() == False): 
                print("wiat for new data in doorbell")
                pass 
            
            mi = doorbell_obj.pick_data_from_doorbell()

            ## the message iterator (mi) is filled with instructions of rigol
            if(mi != None): 
                while(mi.has_next()): 
                    next_instr = mi.next()
                    command_str = next_instr.get_cmd()
                    self.__s.send(command_str.encode())
                    print(command_str)
                    if(next_instr.needs_answer()):
                        # time.sleep(0.1)
                        try: 
                            data = self.__s.recv(self.__buffer_size)
                            self.__recv_data_queue.put(data)
                            # print(data)
                        except: 
                            time.sleep(0.1)
                            print("missed first wait try")
                            print("")
                            try: 
                                data = self.__s.recv(self.__buffer_size)
                                self.__recv_data_queue.put(data)
                                # print(data)
                            except: 
                                time.sleep(0.200)
                                print("missed second wait try")
                                print("")
                                try: 
                                    data = self.__s.recv(self.__buffer_size)
                                    self.__recv_data_queue.put(data)
                                    # print(data)
                                except:
                                    print("missed third wait try")
                                    print("") 
                                    raise
                        # print("message received")
                        # print(data)
                        

            print("end send") 
            print("")

    def get_last_data(self): 
        if(not self.__recv_data_queue.empty()): 
            return self.__recv_data_queue.get()
        else: 
            return None 

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
            # listener.empty_and_inform()
            listener.inform()
            # listener.inform_last()

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


         
        