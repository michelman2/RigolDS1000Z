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
    """
        manages tcp communication operations
    """
    TIME_OUT = 0.00
  
    def __init__(self):
        """
            initializing network connections and settings
            the ip is the autoip assigned to the rigol oscilloscope 
        """
        self.__buffer_size = 250000
        self.__ip = '169.254.16.79'
        self.__port = 5555
        self.__data_ready_list = []
        self.__data_lock = threading.Lock()
        self.__port_listener_list = []
        self.__recv_data_queue = queue.Queue()



    def send_receive_thread(self , doorbell_obj:db.DoorBell):
        """
            sends a message and waits for a response
            should be put in a separate thread
            if the doorbell object has any new message it activates, otherwise the operation is ignored
        """

        while(True): 
            
            while(doorbell_obj.is_data_new() == False): 
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
                        try: 
                            data = self.__s.recv(self.__buffer_size)
                            print("data")
                            next_instr.set_answer(data)
                            # self.__recv_data_queue.put(data)
                            self.__recv_data_queue.put(next_instr)
                            print("after_queue")
                            
                        except: 
                            time.sleep(0.1)
                            print("missed first wait try")
                            try: 
                                data = self.__s.recv(self.__buffer_size)
                                print("data")
                                next_instr.set_answer(data)
                                # self.__recv_data_queue.put(data)
                                self.__recv_data_queue.put(next_instr)
                                
                            except: 
                                time.sleep(0.200)
                                print("missed second wait try")
                                try: 
                                    data = self.__s.recv(self.__buffer_size)
                                    next_instr.set_answer(data)
                                    # self.__recv_data_queue.put(data)
                                    self.__recv_data_queue.put(next_instr)
                                    
                                except:
                                    print("missed third wait try")
                                    print("") 
                                    
                        

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

    def get_data_and_empty_queue(self): 
        last_data = self.get_last_data()
        # self.__recv_data_queue.queue.clear()
        return last_data

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


         
        