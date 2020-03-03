import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
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
from TransactionMeans import DoorBell as db 
import console_thread as ct
import typing
import numpy as np
from decoder import FFTController


""" 
    script handling making of gui. The control part (console) 
    is launched in a separate thread
"""


global UPDATE_GRAPH_AFTER
UPDATE_GRAPH_AFTER = 10


class mclass:
    fourier_transformer = None 
    def __init__(self,  window):
        self.window = window
        self.box = Entry(window)
        self.check_box_state = BooleanVar()
        self.check_button_get_fft = Checkbutton(window, text="check", variable=self.check_box_state)
        self.quit_button = Button(window , text="quit" , command=self.quit)
        self.quit_button.pack()
        self.box.pack()
        self.check_button_get_fft.pack()
        self.fig = None
        self.line = None 
        self.figax = None
        self.oscill_data_tuple = None 

        self.fourier_objects = []
        self.latest_ch3_data = None
        self.latest_ch4_data = None 

        self.ch3_fourier_obj = None
        self.ch4_fourier_obj = None 
        
        ## create second figures
        self.line2 = None 
        self.figax2 = None

        ## create first fft Figure
        self.fft_line1 = None 
        self.fft_ax1 = None

        ##
        self.active_channel = None
        self.data_already_sent_for_fourier = False 
        self.received_frame = False

    def set_observable(self , observable:ct.ConsoleControl): 
        self.observable = observable

    def quit(self): 
        self.window.destroy()
    # def set_fourier_transformer(self , fourier_transofrmer:FFTController.FFTControllerOscillAdapter): 
    #     self.fourier_transformer = fourier_transofrmer

    def get_data_from_observable(self):
        self.window.after(10 , self.get_data_from_observable)
        try: 
            self.oscilloscope_data:rs.cmdObj = self.observable.get_tcp_data()
        except:
            pass 

    # def set_data_for_fourier(self , oscill_data_object): 
    #     self.fourier_transformer.set_oscill_cmd_obj(oscill_data_object)   

    def plot (self):
        
        self.window.after(UPDATE_GRAPH_AFTER , self.plot)         
        
        oscilloscope_data:rs.cmdObj = self.oscilloscope_data
        pause_update = self.check_box_state.get()
                
        if(oscilloscope_data != None): 
            
            if(oscilloscope_data.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.DATA_PAIR): 
            
                if(not pause_update): 
        #             self.data_already_sent_for_fourier = False
        #             self.received_frame = False

        #             x = oscilloscope_data.get_parser().data_idx
        #             y = oscilloscope_data.get_parser().data_val
                    
        #             self.active_channel = oscilloscope_data.get_active_channel()
        #             if(x != None and y != None):                    
        #                 if(self.fig == None): 
        #                     self.fig = Figure()
        #                     self.figax = self.fig.add_subplot(221)
        #                     self.line , = self.figax.plot(x , y)
        #                     self.axvline_11 = plt.axvline(0 , ymin=0 , ymax=100)
        #                     self.axvline_12 = plt.axvline(0 , ymin=0 , ymax=100)
        #                     self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        #                     self.canvas.get_tk_widget().pack()
        #                     self.figax.set_title ("Estimation Grid", fontsize=16)
        #                     self.figax.set_ylabel("Y", fontsize=14)
        #                     self.figax.set_xlabel("X", fontsize=14)
        #                     self.current_y = 1

        #                 if(self.figax2 == None): 
        #                     self.figax2 = self.fig.add_subplot(223)
        #                     self.line2 ,  = self.figax2.plot(x , y)
                            
        #                 if(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH3):
        #                     self.active_channel = None
        #                     self.figax2.set_ylim(np.min(y) , np.max(y))
        #                     self.line2.set_ydata(y) 
        #                     self.line2.set_xdata(x)                   
        #                     self.canvas.draw()
        #                     self.canvas.flush_events()

        #                 elif(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH4): 
        #                     self.active_channel = None 
        #                     self.figax.set_ylim(np.min(y) , np.max(y))
        #                     self.line.set_ydata(y)  
        #                     self.line.set_xdata(x)                  
        #                     self.canvas.draw()
        #                     self.canvas.flush_events()
                    pass
                elif(pause_update):
                    pass
        pass
                    
                    



if(__name__ == "__main__"): 
    print("hellow")
    try: 
        
        console = ct.ConsoleControl()
        console_instance = threading.Thread(target=console.run)
        console_instance.daemon = True 
        
       

        window= Tk()
        start= mclass(window)
        start.set_observable(console) 

        console_instance.start()
       
        window.after(UPDATE_GRAPH_AFTER, start.get_data_from_observable)
        

        window.after(UPDATE_GRAPH_AFTER, start.plot)

        window.mainloop()

        console_instance.

    except: 
        console.finalize_console()
    finally: 
        console.finalize_console()
