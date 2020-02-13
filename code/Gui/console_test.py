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

from Rigol_util import RigolRespProc as rrp
from Rigol_util import channelDataKeeper as cld
from Rigol_util import Rigol_plotter as Rigol_plotter
from Rigol_util import RigolCommander as rc
from doorbell import DoorBell as db 

""" 
    This file tests the console application of doorbell idea 
    The doorbell works the same as a message transfer medium between the tcp 
    connection and the main program

"""


global doorbell_obj # doorbell is shared between main and tcp threads


doorbell_obj = db.DoorBell() # doorbell is used to pass messages between main thread and tcp object

rigol_commander = rc.RigolCommander() # rigol commander helps to create rigol commands more easily

tcp_connection = tcp.TCPcomm() # create an object to handle tcp communication 



try:
    ## create commands
    ## cmd_initiate oscilloscope initializes the commands
    cmd_initiate_oscilloscope = rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
    cmd_ask_data_oscilloscope = rigol_commander.ask_oscilloscope_for_data() # query the oscilloscope for data
    
    cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope) # joining the two commands

    tcp_connection.establish_conn() # establishing a tcp connection with the default ip

    tcp_thread = threading.Thread(target=tcp_connection.send_receive_thread , args=(doorbell_obj,)) # the tcp thread holds tcp connection 
    tcp_thread.daemon = True # keep the thread alive unless the main threads dies 
    tcp_thread.start() # start the thread of tcp connection

    while(True):                
        while(doorbell_obj.is_data_new()):  # check doorbell to see if the message has been picked by tcp ip
            pass 
        cmd_initiate_oscilloscope = rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4) # create init command
        cmd_ask_data_oscilloscope = rigol_commander.ask_oscilloscope_for_data() # query oscilloscope for command
        cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope) # join the commands to create a single one
        doorbell_obj.put_data_to_doorbell(cmd_initiate_oscilloscope) # put data in the doorbell object so the tcp obj can read it
        
        data = tcp_connection.get_last_data() # check the data ready queue of the tcp connection object
        



except:
    tcp_connection.close_conn() # close tcp connection 
    raise 

finally: 
    tcp_connection.close_conn() # close tcp connection 


