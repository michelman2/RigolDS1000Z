import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")
import inspect
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
from TransactionMeans import DoorBell as db 
import console_thread as ct
import typing
import numpy as np
from decoder import FFTController
from debug import debug_instr as dbg

from threading import Lock
from TransactionMeans import LimitedQueue
import time

""" 
    script handling making of gui. The control part (console) 
    is launched in a separate thread
"""


global UPDATE_GRAPH_AFTER
UPDATE_GRAPH_AFTER = 10


class mclass:
    fourier_list_lock = Lock()
    matplot_lock = Lock()
    fourier_transformer = None
    fourier_object_list = []
    fourier_dispatched_queue = LimitedQueue.LimitedQueue(10)
    fourier_finished_queue = LimitedQueue.LimitedQueue(10)
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
        self.canvas = None
        
        self.latest_ch3_data = None
        self.latest_ch4_data = None 


        ##
        self.active_channel = None
        self.data_already_sent_for_fourier = False 
        self.received_frame = False

        ## 
        self.figax_list = []

    def set_observable(self , observable:ct.ConsoleControl): 
        self.observable = observable

    def quit(self): 
        self.window.destroy()
    
    def get_data_from_observable(self):
        while(True): 
            try: 
                self.oscilloscope_data:rs.cmdObj = self.observable.get_tcp_data()
                
            except:
                pass 
            
            
            if(self.oscilloscope_data != None): 
                if(self.oscilloscope_data.get_active_channel() == rs.RIGOL_CHANNEL_IDX.CH3): 
                    # print("************ 3")
                    pass
                    
                elif(self.oscilloscope_data.get_active_channel() == rs.RIGOL_CHANNEL_IDX.CH4): 
                    # print("************ 4")
                    pass
                ## keep the list to a limited size
                # if(len(self.fourier_object_list) < 10): 
                if(self.fourier_dispatched_queue.has_space()): 

                    fft_object = FFTController.FFTControllerOscillAdapter(self.oscilloscope_data,
                                                                        window_duration=1,
                                                                        window_start_time=0,
                                                                        animated=True)
                    

                    fft_object.start_calc_thread()
                    
                    # with self.fourier_list_lock: 
                    #     self.fourier_object_list.append(fft_object)
                    self.fourier_dispatched_queue.put(fft_object)

                

    def read_fourier_list(self):
        while(True):  
            time.sleep(0.1)
            # with self.fourier_list_lock: 
            #     for i in np.arange(0 , len(self.fourier_object_list)): 
            #         current_fourier:FFTController.FFTControllerOscillAdapter = self.fourier_object_list[i]
            #         if(current_fourier.is_operation_done()):
            #             # print("done")
            #             # self.fourier_object_list.pop(i)
            #             # ready_indices.append(i)
            #             pass
            with self.fourier_list_lock: 
                fourier_queue_head:FFTController.FFTControllerOscillAdapter = self.fourier_dispatched_queue.get()
                if(fourier_queue_head.is_operation_done()): 
                    self.fourier_finished_queue.put(fourier_queue_head)
                else: 
                    self.fourier_dispatched_queue.put(fourier_queue_head)
                        
                

    def draw_canvas(self): 
        self.window.after(500 , func=self.draw_canvas)
        if(self.canvas == None): 
            return 
        else: 
            # self.canvas.draw_idle()
            pass

    
    def plot (self):
        
        self.window.after(300 , self.plot)  
        
        oscilloscope_data:rs.cmdObj = self.oscilloscope_data

        pause_update = self.check_box_state.get()
        # pause_update = False
    
        if(oscilloscope_data != None): 
            
            if(oscilloscope_data.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.DATA_PAIR): 
                
                if(not pause_update): 
                    
                    self.data_already_sent_for_fourier = False
                    self.received_frame = False

                    x = oscilloscope_data.get_parser().data_idx
                    y = oscilloscope_data.get_parser().data_val
                    
                    # print("******************** {}".format(len(y)))
                    
                    self.active_channel = oscilloscope_data.get_active_channel()
                    
                    if(x != None and y != None): 
                        
                        if(self.fig == None): 
                            self.fig = Figure()
                            
                            
                            self.ch3_ax = self.fig.add_subplot(221)
                            self.fftch3_ax = self.fig.add_subplot(222)
                            self.ch4_ax = self.fig.add_subplot(223)
                            self.fftch4_ax = self.fig.add_subplot(224)
                            
                            

                            self.ch4_main_line, = self.ch4_ax.plot([0] , [0])
                            self.ch4_vline1 = self.ch4_ax.vlines(x=0 , ymin=-1 , ymax=1)
                            self.ch4_vline2 = self.ch4_ax.vlines(x=0 , ymin=-1 , ymax=1)

                            self.ch3_main_line, = self.ch3_ax.plot([0] , [0])
                            self.ch3_vline1 = self.ch3_ax.vlines(x=0 , ymin=-1 , ymax=1)
                            self.ch3_vline2 = self.ch3_ax.vlines(x=0 , ymin=-1 , ymax=1)

                            self.ch3_fft_line, = self.fftch3_ax.plot([0] , [0])
                            self.ch4_fft_line, = self.fftch4_ax.plot([0] , [0])
                            self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
                            self.canvas.get_tk_widget().pack()
                            
                            self.current_y = 1
                    
                        
                        if(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH3):
                            # print("**************** {}".format(self.active_channel))
                            # pass 
                            self.active_channel = None
                            
                            self.ch3_ax.set_ylim(np.min(y) , np.max(y))
                            self.ch3_ax.set_xlim(np.min(x) , np.max(x))
                            self.ch3_main_line.set_xdata(x)
                            self.ch3_main_line.set_ydata(y)
                            # print("---------------- reached end 1")
                            
                            # self.canvas.draw()
                            # 
                        #     self.canvas.flush_events()

                        elif(self.active_channel == rs.RIGOL_CHANNEL_IDX.CH4):
                            # print("**************** {}".format(self.active_channel))
                            self.active_channel = None 
                            self.ch4_ax.set_ylim(np.min(y) , np.max(y))
                            self.ch4_ax.set_xlim(np.min(x) , np.max(x))
                            self.ch4_main_line.set_xdata(x)
                            self.ch4_main_line.set_ydata(y)   

                            # print("---------------- reached end 2") 
                            # self.canvas.draw()
                        #     self.canvas.flush_events()

                        # self.canvas.draw()
                        
        pass
                    
                    



if(__name__ == "__main__"): 
    dbg.flags.cond_print("hellow")
    try: 
        
        console = ct.ConsoleControl()
        console_instance = threading.Thread(target=console.run)
        console_instance.daemon = True 
        
        

        window= Tk()
        start= mclass(window)
        start.set_observable(console) 

        console_instance.start()
        
        get_observable_data = threading.Thread(target=start.get_data_from_observable)
        get_observable_data.daemon = True 
        get_observable_data.start()

        
                
        fourier_checker_thread = threading.Thread(target=start.read_fourier_list)
        fourier_checker_thread.daemon = True
        fourier_checker_thread.start()

        window.after(300 , start.plot)
        window.after(400 , start.draw_canvas)
        
        window.mainloop()
        print("closed normally")  

    except: 
        console.finalize_console()
    finally: 
        console.finalize_console()
