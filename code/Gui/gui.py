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
import console_thread as ct
import typing


""" 
    script handling making of gui. The control part (console) 
    is launched in a separate thread
"""


global UPDATE_GRAPH_AFTER
UPDATE_GRAPH_AFTER = 20

class mclass:
    def __init__(self,  window):
        self.window = window
        self.box = Entry(window)
        self.button = Button (window, text="check", command=self.plot)
        self.box.pack ()
        self.button.pack()
        self.fig = None
        self.line = None 
        self.figax = None
        
        ## create second figures
        self.line2 = None 
        self.figax2 = None

        ##
        self.active_channel = None

    def set_observable(self , observable:ct.ConsoleControl): 
        self.observable = observable

    def plot (self):
        self.window.after(UPDATE_GRAPH_AFTER , self.plot)
         
        
        command_obj:rs.cmdObj = self.observable.get_data_and_empty_queue()
        
        
        if(command_obj != None): 
            ## check to see if data parser is data_pair
            if(command_obj.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.DATA_PAIR): 
                x = command_obj.get_parser().data_idx
                y = command_obj.get_parser().data_val

                if(x != None and y != None):                    
                    if(self.fig == None): 
                        self.fig = Figure()
                        self.figax = self.fig.add_subplot(211)
                        self.line , = self.figax.plot(x , y)
                        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
                        self.canvas.get_tk_widget().pack()
                        self.figax.set_title ("Estimation Grid", fontsize=16)
                        self.figax.set_ylabel("Y", fontsize=14)
                        self.figax.set_xlabel("X", fontsize=14)
                        self.current_y = 1

                    if(self.figax2 == None): 
                        self.figax2 = self.fig.add_subplot(212)
                        self.line2 ,  = self.figax2.plot(x , y)
                        
                    if(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH3): 
                        self.active_channel = None
                        self.line2.set_ydata(y)                    
                        self.canvas.draw()
                        self.canvas.flush_events()

                    elif(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH4): 
                        self.active_channel = None 
                        self.line.set_ydata(y)                    
                        self.canvas.draw()
                        self.canvas.flush_events()

            elif(command_obj.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.PREAMBLE): 
                pass 

            elif(command_obj.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.CHANNEL_NUMBER): 
                # print("channel_number {}".format(command_obj.get_parser().get_channel()))
                self.active_channel = command_obj.get_parser().get_channel() 
            

if(__name__ == "__main__"): 
    print("hellow")
    try: 
        
        console = ct.ConsoleControl()
        console_instance = threading.Thread(target=console.run)
        console_instance.daemon = True 
        console_instance.start()
        

        window= Tk()
        start= mclass(window)
        start.set_observable(console)
        window.after(UPDATE_GRAPH_AFTER, start.plot)
        window.mainloop()

    except: 
        ## handling finalizing operation in the console thread
        console.finalize_console()
    finally: 
        ## handling finalizing operations in the console thread
        console.finalize_console()
