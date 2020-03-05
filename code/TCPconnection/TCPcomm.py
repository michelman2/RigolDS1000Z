import socket 
import threading
import enum
import MessageIterables as mes_iter
import time 
from inspect import getframeinfo , currentframe
import typing
import TransactionMeans.DoorBell as db
import queue
import tcp_queue
from print_util import print_colors
from termcolor import colored
from decoder import SineCreator
from debug import debug_instr as dbg

class TCPcomm(threading.Thread):    
    """
        manages tcp communication operations
    """
    
    if(dbg.flags.LOOPBACK): 
        print("Warning loopback MODE ON in TCP COMM")
    

    TIME_OUT = 0.00
  
    def __init__(self):
        """
            initializing network connections and settings
            the ip is the autoip assigned to the rigol oscilloscope 
        """
        self.__buffer_size = 250000
        self.__ip = '169.254.16.78'
        self.__port = 5555
        self.__data_ready_list = []
        self.__data_lock = threading.Lock()
        self.__port_listener_list = []
        self.__recv_data_queue = queue.Queue()
        self.__recv_queue_max_limit = 20
        # self.__recv_data_queue = tcp_queue.tcp_queue(queue_space_limit=5)



    def send_receive_thread(self , doorbell_obj:db.DoorBell):
        """
            sends a message and waits for a response
            should be put in a separate thread
            if the doorbell object has any new message it activates, otherwise the operation is ignored
        """

        while(True): 
            time.sleep(0.1)
            while(doorbell_obj.is_data_new() == False): 
                pass 
            
            mi = doorbell_obj.pick_data_from_doorbell()

            ## the message iterator (mi) is filled with instructions of rigol
            if(mi != None):
                dbg.flags.cond_print("rec queue size : {}".format(self.__recv_data_queue.qsize()))
                if(self.__recv_data_queue.qsize() > self.__recv_queue_max_limit):
                    self.__recv_data_queue.get()
                while(mi.has_next()): 
                    next_instr = mi.next()
                    command_str = next_instr.get_cmd()
                    # self.__s.send(command_str.encode())
                    self.tcp_send_wrapper(command_str.encode())
                    dbg.flags.cond_print(command_str)
                    if(next_instr.needs_answer()):
                        try: 
                            # self.__s.settimeout(0.1)
                            self.tcp_set_timeout_wrapper(0.1)

                            # data = self.__s.recv(self.__buffer_size)
                            data = self.tcp_recv_wrapper(self.__buffer_size)

                            next_instr.set_answer(data)
                            # self.__recv_data_queue.put(data)
                            self.__recv_data_queue.put(next_instr)
                            dbg.flags.cond_print("after_queue")
                            
                        except: 
                            # time.sleep(0.1)
                            dbg.flags.cond_print("missed first wait try")
                            try: 
                                data = self.__s.recv(self.__buffer_size)
                                dbg.flags.cond_print("data")
                                next_instr.set_answer(data)
                                # self.__recv_data_queue.put(data)
                                self.__recv_data_queue.put(next_instr)
                                
                            except: 
                                # time.sleep(0.2)
                                dbg.flags.cond_print("missed second wait try")
                                try: 
                                    data = self.__s.recv(self.__buffer_size)
                                    next_instr.set_answer(data)
                                    # self.__recv_data_queue.put(data)
                                    self.__recv_data_queue.put(next_instr)
                                    
                                except:
                                    dbg.flags.cond_print("missed third wait try")
                                    dbg.flags.cond_print("") 
                                    
                        

            dbg.flags.cond_print("end send") 
            dbg.flags.cond_print("")

    def get_last_data(self):
        dbg.flags.cond_print("in get last data") 
        # if(not self.__recv_data_queue.empty()): 
        return self.__recv_data_queue.get()
        # else: 
        #     return None 

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

    def tcp_send_wrapper(self, message): 
        """ 
            tcp send wrapper to add probing with loopback 
        """ 
        if(dbg.flags.LOOPBACK):
            pass 
        else:  
            self.__s.send(message)

    def tcp_set_timeout_wrapper(self , number): 
        """ 
            A wrapper function to add loopback functionality
        """
        if(dbg.flags.LOOPBACK): 
            pass 
        else: 
            self.__s.settimeout(number)

    def tcp_recv_wrapper(self , buffer_size): 
        """ 
            If loopback is on, the tcp is cut off and a sinosoid is returned
        """
        if(dbg.flags.LOOPBACK): 
            sc = SineCreator.SineCreator()
            getsine = sc.create_sine(number_of_samples = 5000 ,
                                    time_frequency = 1 , 
                                    time_length = 2 ,
                                    init_phase_degree = 40 )
            getsine2 = sc.create_sine(number_of_samples = 5000,
                                    time_frequency = 5 , 
                                    time_length = 2, 
                                    init_phase_degree=0)



            mixed_sine = sc.mix_sines([getsine , getsine2] , 2)
            return mixed_sine

        else: 
            return self.__s.recv(buffer_size)

    def get_data(self): 
        
        if(self.__recv_data_queue.qsize()>0): 
            return self.__recv_data_queue.get()
        else: 
            return None 
        
        

    def establish_conn(self):
        """ 
            If the loopback mode is on, no actual connection to a socket needs to be made
        """
        if(dbg.flags.LOOPBACK): 
            pass 
        else: 
            try: 
                self.__s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                self.__s.setblocking(1)          
                self.__s.connect((self.__ip , self.__port))
                self.__s.settimeout(self.TIME_OUT)
            except: 
                self.__s.close()
                raise 

    def close_conn(self): 
        if(dbg.flags.LOOPBACK):
            pass 
        else: 
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


         
        