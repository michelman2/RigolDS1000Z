import socket 
import threading
import enum
import MessageIterables as mes_iter
import time 

# message = '*idn?\n'.encode()

class TCPcomm(threading.Thread):    

    TIME_OUT = 0.5
    def __init__(self): 
        self.__buffer_size = 250000
        self.__ip = '169.254.16.78'
        self.__port = 5555

    def run(self , message_object): 
        # if(not isinstance(message_object , mes_iter.MessageIterable)): 
        #     raise TypeError
        try: 
            s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            s.setblocking(0)
            s.settimeout(self.TIME_OUT)
            s.connect((self.__ip , self.__port))
            ## message_object implements the MessageIterables.py 
            while(message_object.has_next()): 
                current_message = message_object.next()
                st_tstamp = time.time()
                s.send(current_message.encode())
                data = "nothing received in the timeout span"
                try:                     
                    data = s.recv(self.__buffer_size)
                    end_tstamp = time.time()
                    print("time {}".format(end_tstamp - st_tstamp))
                    print("message len {}".format(len(data)))
                except: 
                    pass 
                 
                print(data)
            
            s.close()
        except: 
            s.close()
            raise

    def set_ip(self , ip):
        self.__ip = ip

    def set_port(self , port): 
        self.__port = port

    def set_buffer_size(self , buffer_size): 
        self.__buffer_size = buffer_size

    def set_message(self , message):
        if(not isinstance(message , mes_iter.MessageIterable)): 
            raise TypeError



