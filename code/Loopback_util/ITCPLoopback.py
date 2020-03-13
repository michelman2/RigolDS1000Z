"""
    Loopback interface for rigol tcp devices
    The loopback is meant to be placed as a tcp devices
    The interface is the same as tcp devices
"""

import abc

class ITCPloopback(abc.ABC): 

    """ The following methods are only placeholders when 
        creating loopback features, as there is no real 
        connection being made with a physical device
    """
    
    def settimeout(self , *args): 
        pass 
    def socket(self , *args): 
        pass 
    def socketpair(self , *args): 
        pass 
    def create_connection(self , *args): 
        pass 
    def create_server(self , *args): 
        pass 
    def has_dualstack_ipv6(self , *args): 
        pass 
    def fromfd(self , *args): 
        pass 
    def setdefaulttimeout(self , *args): 
        pass 
    def accept(self , *args): 
        pass 
    def bind(self , *args): 
        pass 
    def close(self , *args): 
        pass 
    def connect(self , *args): 
        pass
    def connect_ex(self , *args): 
        pass 
    def detach(self , *args): 
        pass 
    def dup(self , *args): 
        pass 
    def getblocing(self , *args): 
        pass 
    def gettimeout(self , *args): 
        pass
    def listen(self , *args): 
        pass 
    # def recv(self , *args): 
    #     pass 
    def recvfrom(self , *args): 
        pass 
    def recvmsg(self , *args): 
        pass 
    # def send(self , *args): 
    #     pass 
    def sendall(self , *args): 
        pass 
    def sendto(self , *args): 
        pass 
    def sendmsg(self , *args): 
        pass 
    

    """
        The following functions should be implemented.  
    """
    @abc.abstractmethod
    def recv(self , buff_size , *flags): 
        pass 

    @abc.abstractmethod
    def send(self , bytes , *flags): 
        pass 




    