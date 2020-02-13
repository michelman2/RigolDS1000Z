import subprocess
import re
import platform
import socket
import threading 


"""
    searching tools for finding the ip address of oscilloscope
    too slow to be done every time
""" 

class IPIterator: 
    """
        Tools for iterating in ip ranges 
    """

    def __init__(self): 
        if(platform.system() == "Windows"): 
            ipcommand = "ipconfig"
        else: 
            ipcommand = "ifconfig"

        proc = subprocess.check_output(ipcommand).decode("utf-8")

        self.lines = proc.split('\n')

        self.list_to_find = ["Connection-specific DNS Suffix", 
            "Link-local IPv6 Address", 
            "Autoconfiguration IPv4 Address", 
            "Subnet Mask", 
            "Default Gateway"]

        self.found_ethernet_field = False
        self.fields_to_find = 2
        self.ipv4 = []
        self.sub_mask = []
        self.thread_list = []

        self.__PING_DELAY = 1

        

    def init(self): 
        """ 
            searching the response of ifconfig to find ethernet connection 
            ip and submask
        """
        found_fields = 0
        for line in self.lines:     
            if(line.lower().find("ethernet") != -1): 
                self.found_ethernet_field = True

            if(self.found_ethernet_field == True): 
                if(line.find(self.list_to_find[2]) != -1):
                    found_fields += 1  
                    self.ipv4 = ip(self.find_ip(line))

                if(line.find(self.list_to_find[3]) != -1):
                    found_fields += 1
                    self.sub_mask = ip(self.find_ip(line))                    

                if(found_fields >= self.fields_to_find): 
                    break


    def find_ip(self , line:str)->re.Match: 
        """
            looking for ip addresses in the lines found from ethernet fields
        """
        obj = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" , line).group()
        split_ip = obj.split(".")
        int_list_ip = [int(x) for x in split_ip]
        return int_list_ip

    def __make_ip(self,ip_list, idx , ip_part)->list:
        """
            generate an ip based on the input parameters
            ip_list is the initial ip 
            idx: the index of the ip field 0 to 3
            ip_part: ip value of the part whose index is given in idx
        """
        if(self.sub_mask.get()[idx] == 255): 
            ip_list[idx] = self.ipv4.get()[idx]
        else: 
            ip_list[idx] = ip_part

        return ip_list


    def __tcp_test(self , ip, port_number, delay): 
        """
            checks an ip number and port for connection

        """
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.setblocking(0)
        TCPsock.settimeout(1)
        # TCPsock.settimeout(20)
        try:
            TCPsock.connect((ip, port_number))
            # output[port_number] = 'Listening'
            print("{}: open".format(ip))
        except:
            print(ip)
            # output[port_number] = ''
            TCPsock.close()
        
        # print(ip)
        TCPsock.close()


    

    def iterate(self): 
        iterate_ip = [0,0,0,0]
        submask = self.sub_mask.get()
        for i_0 in range(0,255-submask[0] + 1): 
            iterate_ip = self.__make_ip(iterate_ip , 0 , i_0)   
            
            for i_1 in range(0 , 255-submask[1] + 1):
                iterate_ip = self.__make_ip(iterate_ip , 1 , i_1)

                for i_2 in range(0 , 255-submask[2] + 1): 
                    iterate_ip = self.__make_ip(iterate_ip , 2 , i_2)
                    
                    for i_3 in range(0 , 255-submask[3] + 1):
                        iterate_ip = self.__make_ip(iterate_ip , 3 , i_3) 
                        str_ip = "{}.{}.{}.{}".format(iterate_ip[0], iterate_ip[1],iterate_ip[2],iterate_ip[3])
                        ip_thread = threading.Thread(target=self.__tcp_test ,
                            args=(str_ip,5555,self.__PING_DELAY))
                        self.thread_list.append(ip_thread)

        print("done assigning threads")
        started_threads_cnt = 0
        thread_group_idx = 0
        THREAD_GROUP_CNT = 1000
        while(started_threads_cnt < len(self.thread_list)):

            for idx_in_thread_group in range(0 , THREAD_GROUP_CNT): 
                thread_idx = thread_group_idx * THREAD_GROUP_CNT + idx_in_thread_group
                self.thread_list[thread_idx].start()
                started_threads_cnt += 1

            for idx_in_thread_group in range(0 , THREAD_GROUP_CNT): 
                thread_idx = thread_group_idx * THREAD_GROUP_CNT + idx_in_thread_group
                self.thread_list[thread_idx].join()
                
            
            
            thread_group_idx += 1
            print(started_threads_cnt)              
        


class ip: 
    ## holding ip address

    def __init__(self , int_list:list): 
        self.__ip = int_list

    def get(self): 
        return self.__ip

    


    

a = IPIterator()
a.init()
a.iterate()