import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import threading

import Rigol_Lib.RigolSCPI as rs
import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp
import TCPconnection.TCPListener as tl

# from Rigol_util import RigolRespProc as rrp
from Rigol_util import channelDataKeeper as cld
# from Rigol_util import Rigol_plotter as Rigol_plotter
from Rigol_util import RigolCommander as rc
from doorbell import DoorBell as db 
import time


class ConsoleControl: 
    """ 
        A wrapper class to put the console application and its functionality 
        in a single object. This class launches threads to handle tcp connection. 

        Can be used as the main thread when using none-gui applications
        Can be launched in a second thread (the run method) when using gui applications

    """
    
    global doorbell_obj # doorbell objet is used between the thread running this class and the thread handling tcp connections



    def __init__(self):
        # create doorbell object for message passing between main thread
        # and the single thread
        self.doorbell_obj = db.DoorBell()

        ## create commander object to manage generation of commands
        self.rigol_commander = rc.RigolCommander()

        ## create tcp object: manages send, receive, connection
        self.tcp_connection = tcp.TCPcomm()

        self.__pause_tcp_conn = False

    def run(self):
        
        try:
            
            ## create commands: 
            cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
            cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
            ## join two commands: 
            cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)

            ## start a tcp connection
            self.tcp_connection.establish_conn()

            ## we only have two threads: 1 main and the other one for tcpip
            self.tcp_thread = threading.Thread(target=self.tcp_connection.send_receive_thread , args=(self.doorbell_obj,))
            self.tcp_thread.daemon = True
            self.tcp_thread.start()

            latest_channel = rs.RIGOL_CHANNEL_IDX.CH4
            while(True):
                if(self.pause_tcp_connection):                     
                    while(self.doorbell_obj.is_data_new()):
                        pass

                    if(latest_channel == rs.RIGOL_CHANNEL_IDX.CH3):  
                        latest_channel = rs.RIGOL_CHANNEL_IDX.CH4

                    elif(latest_channel == rs.RIGOL_CHANNEL_IDX.CH4): 
                        latest_channel = rs.RIGOL_CHANNEL_IDX.CH3
                        


                    cmd_initiate_oscilloscope = self.rigol_commander.initalize_data_query_byte(latest_channel)
                    cmd_ask_active_channel = self.rigol_commander.ask_for_active_channel()
                    cmd_ask_data_oscilloscope = self.rigol_commander.ask_oscilloscope_for_data()
                    
                    cmd_initiate_oscilloscope.append(cmd_ask_active_channel)
                    cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)
                    
                    
                
                    self.doorbell_obj.put_data_to_doorbell(cmd_initiate_oscilloscope)   ## put date to doorbell
                    
                    time.sleep(0.3) ## add time delay to reduce cpu usage
                    

        

        except:
            self.tcp_connection.close_conn() 
            raise 

        finally: 
            self.tcp_connection.close_conn()

    def get_data(self): 
        return self.tcp_connection.get_last_data()

    def get_data_and_empty_queue(self): 
        return self.tcp_connection.get_data_and_empty_queue() 

    def pause_tcp_connection(self): 
        self.__pause_tcp_conn = True

    def resume_tcp_connection(self): 
        self.__pause_tcp_conn = False

    def finalize_console(self):
        self.tcp_connection.close_conn()