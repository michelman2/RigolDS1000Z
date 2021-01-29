import socket 
import threading
import enum
from TransactionMeans import MessageCarrier
import time 
from inspect import getframeinfo , currentframe
import typing
import TransactionMeans.DoorBell as db
import queue
from decoder import SineCreator
from debug import debug_instr as dbg
from Rigol_Lib import RigolSCPI as rs 
from Loopback_util import RigolOscillLB


class TCPcomm(threading.Thread):    
    """
        manages tcp communication operations
    """
    TIME_OUT = 0 
  
    def __init__(self, ip , port , buff_size = 250000, single_run = False):
        """
            initializing network connections and settings
            the ip is the autoip assigned to the rigol oscilloscope 
        """
        self._s = None 
        self._buffer_size = buff_size
        self._ip = ip 
        self._port = port 
        self._is_single_run = single_run
        self._data_ready_list = []
        self._data_lock = threading.Lock()
        self._port_listener_list = []
        self._recv_data_queue = queue.Queue()
        self._recv_queue_max_limit = 20
        


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
                dbg.flags.cond_print("rec queue size : {}".format(self._recv_data_queue.qsize()))
                if(self._recv_data_queue.qsize() > self._recv_queue_max_limit):
                    self._recv_data_queue.get()
                for next_instr in mi: 
               
                    command_str = next_instr.get_cmd()
                    self._s.send(command_str.encode())
                    dbg.flags.cond_print(command_str)
                    
                    if(next_instr.needs_answer()):
                        try: 
                            self._s.settimeout(0.3)

                            data = self._s.recv(self._buffer_size)
                            
                            next_instr.set_answer(data)
                            
                            self._recv_data_queue.put(next_instr)
                            dbg.flags.cond_print("after_queue")
                            
                        except: 

                            time.sleep(0.1)
                            dbg.flags.cond_print("missed first wait try")
                            try: 
                                data = self._s.recv(self._buffer_size)
                                
                                dbg.flags.cond_print("data")
                                next_instr.set_answer(data)
                                # self._recv_data_queue.put(data)
                                self._recv_data_queue.put(next_instr)
                                
                            except: 
                                time.sleep(0.2)
                                dbg.flags.cond_print("missed second wait try")
                                try: 
                                    data = self._s.recv(self._buffer_size)
                                    
                                    next_instr.set_answer(data)
                                    # self._recv_data_queue.put(data)
                                    self._recv_data_queue.put(next_instr)
                                    
                                except:
                                    dbg.flags.cond_print("missed third wait try")
                                    dbg.flags.cond_print("") 
                                    
                        

            dbg.flags.cond_print("end send") 
            dbg.flags.cond_print("")

    def get_last_data(self):
        dbg.flags.cond_print("in get last data") 
        # if(not self._recv_data_queue.empty()): 
        return self._recv_data_queue.get()
        # else: 
        #     return None 

    ## Implementation of observer pattern
    def subscribe_listener(self , listener): 
        ## A listener is an object that implements an inform() method
        ## and can reuest subscription to the tcp comm object
        with self._data_lock: 
            self._port_listener_list.append(listener)

   
    def get_data(self): 
        
        if(self._recv_data_queue.qsize()>0): 
            return self._recv_data_queue.get()
        else: 
            return None 
        
        

    def establish_conn(self):
        """ 
            If the loopback mode is on, no actual connection to a socket needs to be made
        """
        
        try: 
            if(dbg.flags.LOOPBACK): 
                self._s = RigolOscillLB.RigolOscillLB()

            else:
                self._s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                self._s.setblocking(1)          
                self._s.connect((self._ip , self._port))
                self._s.settimeout(self.TIME_OUT)

        except:
            if(self._s != None): 
                self._s.close()
            raise 

    def close_conn(self): 
        self._s.close()
        
    def set_ip(self , ip):
        self._ip = ip

    def set_port(self , port): 
        self._port = port

    def set_buffer_size(self , buffer_size): 
        self._buffer_size = buffer_size


         


        