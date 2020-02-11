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



global doorbell_obj




# create doorbell object for message passing between main thread
# and the single thread
doorbell_obj = db.DoorBell()

## create commander object to manage generation of commands
rigol_commander = rc.RigolCommander()

## create tcp object: manages send, receive, connection
tcp_connection = tcp.TCPcomm()



try:
    ## create commands: 
    cmd_initiate_oscilloscope = rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
    cmd_ask_data_oscilloscope = rigol_commander.ask_oscilloscope_for_data()
    ## join two commands: 
    cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)

    ## start a tcp connection
    tcp_connection.establish_conn()

    ## we only have two threads: 1 main and the other one for tcpip
    tcp_thread = threading.Thread(target=tcp_connection.send_receive_thread , args=(doorbell_obj,))
    tcp_thread.daemon = True
    tcp_thread.start()

    while(True):
        # if(pause_tcp_connection):                     
        while(doorbell_obj.is_data_new()):
            # print("inside wait for doorbell to be seen")
            pass 
        cmd_initiate_oscilloscope = rigol_commander.initalize_data_query_byte(rs.RIGOL_CHANNEL_IDX.CH4)
        cmd_ask_data_oscilloscope = rigol_commander.ask_oscilloscope_for_data()
        cmd_initiate_oscilloscope.append(cmd_ask_data_oscilloscope)
        doorbell_obj.put_data_to_doorbell(cmd_initiate_oscilloscope)
        
        data = tcp_connection.get_last_data()
        print(data)



except:
    tcp_connection.close_conn() 
    raise 

finally: 
    tcp_connection.close_conn()


