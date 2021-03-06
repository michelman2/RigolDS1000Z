
import __init__

from PyQt5 import QtCore, QtGui
import pyqtgraph as pg


import numpy as np

import Rigol_Lib.RigolSCPI as rs
from TransactionMeans import MessageCarrier as mi
import TCPconnection.TCPcomm as tcp

from Rigol_util import channelDataKeeper as cld
from Rigol_util import RigolCommander as rc
from TransactionMeans import DoorBell as db
import TransactionMeans 
import console_thread as ct
import typing
import numpy as np
from decoder import FFTController
from debug import debug_instr as dbg

import threading
from threading import Lock
from TransactionMeans import LimitedQueue
import time



class MainWindow(QtGui.QMainWindow):

    fourier_list_lock = Lock()
    matplot_lock = Lock()
    fourier_transformer = None
    fourier_object_list = []
    fourier_dispatched_queue = LimitedQueue.LimitedQueue(10)
    fourier_finished_queue = LimitedQueue.LimitedQueue(10)
    oscilloscope_data = None
    
    vlines_min_per_ch = [None , None , None , None]
    vlines_max_per_ch = [None , None , None , None]

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.login_widget.check_box.stateChanged.connect(self.box_state_checker)
        self.central_widget.addWidget(self.login_widget)
        self.timer = QtCore.QTimer()

    def box_state_checker(self): 
        print("checkded")
        if(self.login_widget.getRunFFT()): 
            self.timer.setInterval(40)
            pass
        else: 
            self.timer.setInterval(40)

    def plotter(self):
        self.data =[0]
        
       
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)

    def getGraphCanvas(self): 
        """ 
            test: return only one graph instance of curves
            When no test: returns a multidimensional list of curves in gui
        """
        # return self.login_widget.getCurves()[0][0]
        return self.login_widget.getCurves()
    
    def updater(self):        

        curves = self.login_widget.getCurves()
        vline1_curves = self.login_widget.getVline1Curves()
        vline2_curves = self.login_widget.getVline2Curves()

        oscilloscope_data:rs.cmdObj = self.oscilloscope_data
        
        pause_update = self.login_widget.getRunFFT()

        
        if(oscilloscope_data != None):
            if(oscilloscope_data.get_parser().get_response_type() == rs.SCPI_RESPONSE_TYPE.DATA_PAIR): 
                if(not pause_update):
                    self.fourier_ready_list= [None , None , None , None]
                    self.fourier_frames = [None , None , None , None]
                
                    
                    x = oscilloscope_data.get_parser().get_data_x()
                    y = oscilloscope_data.get_parser().get_data_y()
                    
                    self.active_channel = oscilloscope_data.get_active_channel()

                    if(x != None and y!= None): 
                        
                        curves[self.active_channel.get_data_val()][0].setData(x , y)
                        

                else:
                    try: 
                        fourier_ready:FFTController.FFTControllerOscillAdapter = self.fourier_finished_queue.get_nowait()
                    except: 
                        fourier_ready = None
                        pass 

                    if(fourier_ready != None): 
                        current_fourier_channel = fourier_ready.get_command_object().get_active_channel().get_data_val()
                        
                        if(self.fourier_ready_list[current_fourier_channel] == None):
                            self.fourier_ready_list[current_fourier_channel] = fourier_ready
                            self.fourier_frames[current_fourier_channel] = fourier_ready.get_iterable_frames()
                            x = fourier_ready.get_command_object().get_parser().get_data_x_idx()
                            y = fourier_ready.get_command_object().get_parser().get_data_y_idx()
                            self.vlines_min_per_ch[current_fourier_channel] = np.min(y)
                            self.vlines_max_per_ch[current_fourier_channel] = np.max(y)
                            curves[current_fourier_channel][0].setData(x , y)

                    
                    for idx , fourier_frame_iterable in enumerate(self.fourier_frames): 
                        if(fourier_frame_iterable != None):
                            if(fourier_frame_iterable.has_next()): 
                                fourier_frame = fourier_frame_iterable.next()
                                fourier_x = fourier_frame[0][0]
                                fourier_y = fourier_frame[0][1]
                                fourier_win_start = fourier_frame[1][0]
                                fourier_win_end = fourier_frame[1][1]
                                curves[idx][1].setData(fourier_x[10:] , fourier_y[10:])
                                
                            
                                vline1_curves[idx][0].setData([fourier_win_start , fourier_win_start] ,
                                                            [self.vlines_min_per_ch[idx] , self.vlines_max_per_ch[idx]])
                                vline2_curves[idx][0].setData([fourier_win_end , fourier_win_end], 
                                                            [self.vlines_min_per_ch[idx] , self.vlines_max_per_ch[idx]])
                   
        
    

    # def read_fourier_list(self):
    #     while(True):  
    #         time.sleep(0.1)
            
    #         with self.fourier_list_lock: 
    #             fourier_queue_head:FFTController.FFTControllerOscillAdapter = self.fourier_dispatched_queue.get()
    #             if(fourier_queue_head.is_operation_done()): 
    #                 self.fourier_finished_queue.put(fourier_queue_head)
    #             else: 
    #                 self.fourier_dispatched_queue.put(fourier_queue_head)
                        
                

class LoginWidget(QtGui.QWidget):
    
    curves = []
    plots = []
    vline1_curves = []
    vline2_curves = []


    def getCurves(self): 
        return self.curves

    def getVline1Curves(self): 
        return self.vline1_curves

    def getVline2Curves(self): 
        return self.vline2_curves

    def getPlotters(self): 
        return self.plots

    def getRunFFT(self): 
        return self.check_box.isChecked()

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        ## create a control button
        self.button = QtGui.QPushButton('Start Plotting')
        
        ## create a checkbox
        self.check_box = QtGui.QCheckBox("run fft")

        ## A vertical layout box for putting control widgets
        self.control_column = QtGui.QVBoxLayout()
        self.control_column.addWidget(self.button)
        self.control_column.addWidget(self.check_box)

        ## A vertical layout box for holding horizontal graph layouts
        self.graph_column = QtGui.QVBoxLayout()

        self.graph_pair_row = [QtGui.QHBoxLayout() for i in range(4)]
        _ = [self.graph_column.addLayout(self.graph_pair_row[i]) for i in range(len(self.graph_pair_row))]
        
        
 
        ## create main panel layout
        self.main_panel_layout = QtGui.QHBoxLayout()
        self.main_panel_layout.addLayout(self.control_column)
        self.main_panel_layout.addLayout(self.graph_column)
 

        for i in range(len(self.graph_pair_row)): 
            plots_in_current_row = []
            curves_in_current_row = []
            vline1_curves_in_current_row = []
            vline2_curves_in_current_row = []
            for j in range(2): 
                plotter = pg.PlotWidget()
                
                self.graph_pair_row[i].addWidget(plotter)
                plots_in_current_row.append(plotter)
                curves_in_current_row.append(plotter.getPlotItem().plot())
                vline1_curves_in_current_row.append(plotter.getPlotItem().plot())
                vline2_curves_in_current_row.append(plotter.getPlotItem().plot())

            self.curves.append(curves_in_current_row) 
            self.plots.append(plots_in_current_row)
            self.vline1_curves.append(vline1_curves_in_current_row)
            self.vline2_curves.append(vline2_curves_in_current_row)
            
        self.setLayout(self.main_panel_layout)
