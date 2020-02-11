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
import console_thread as ct
import typing

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
        self.ch4_dataholder = cld.channelDataKeeper(rs.RIGOL_CHANNEL_IDX.CH4)

    def set_observable(self , observable:ct.ConsoleControl): 
        self.observable = observable

    def plot (self):
        self.window.after(UPDATE_GRAPH_AFTER , self.plot)
        # x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        # v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        # p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
        #     19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])
        
        data = self.observable.get_data()
        if(data != None): 
            
            rigol_resp = rrp.RigolRespProc(data)
            extracted_data = rigol_resp.getHeader()
            self.ch4_dataholder.set_data(extracted_data)

            x = self.ch4_dataholder.get_data_idx()
            y = self.ch4_dataholder.get_data_value()
            
            if(x != None and y != None):                    
                if(self.fig == None): 
                    # self.fig = Figure(figsize=(6,6))
                    self.fig = Figure()
                    self.figax = self.fig.add_subplot(111)
                    self.line , = self.figax.plot(x , y)
                    self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
                    self.canvas.get_tk_widget().pack()
                    self.figax.set_title ("Estimation Grid", fontsize=16)
                    self.figax.set_ylabel("Y", fontsize=14)
                    self.figax.set_xlabel("X", fontsize=14)
                    self.current_y = 1

                self.line.set_ydata(y)
                
                self.canvas.draw()
                self.canvas.flush_events()



if(__name__ == "__main__"): 

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
