import __init__ 

from PyQt5 import QtCore, QtGui
import pyqtgraph as pg

import numpy as np

from Rigol_Lib import RigolSCPI as rs
import TCPconnection.TCPcomm as tcp

from Rigol_util import channelDataKeeper as cld
from Rigol_util import RigolCommander as rc
from TransactionMeans import DoorBell as db
import console_thread as ct
import typing
import numpy as np
from decoder import FFTController
from debug import debug_instr as dbg
from Gui import pyqt_gui
from Gui import bundleManager
from PyQt5 import QtCore
import threading
from threading import Lock
from TransactionMeans import LimitedQueue
from TransactionMeans import MessageCarrier
from TransactionMeans import MeaningfulList
import time

class GuiLogicGlue: 
    def __init__(self):
        self._update_timer = QtCore.QTimer()
        self._update_timer.timeout.connect(self.update_gui)
        self._app = QtGui.QApplication([])
        self._window = pyqt_gui.MainWindow()
        ## logic creation
        self._console:ct.ConsoleControl = ct.ConsoleControl()
        self._console_thread = threading.Thread(target=self._console.run)
        self._console_thread.daemon = True 

        ## setup glue between logic and gui: 
        self._bundle_group = bundleManager.BundlersGroup()
        bundling_strategy = bundleManager.RowWiseBundler()
        self._bundle_group.set_bundler_strategy(bundling_strategy)
        bundlers_from_logic = self._console.get_data_gui_bundlers()
        self._bundle_group.set_bundlers_list(bundlers_from_logic)
        
        canvas_list_from_gui = MeaningfulList.MeaningfulList.from_list(self._window.getGraphCanvas())
        ## glue
        self._bundle_group.set_canvas(canvas_list_from_gui)
        self._bundle_group.bundle_all_to_canvas()
        
        self._window.show()
        

    def update_gui(self): 
        self._bundle_group.update_all()
      
    def startApp(self): 
        self._console_thread.start()
        self._update_timer.start(50)
        self._app.exec_()


try: 
    gui_glue = GuiLogicGlue()
    gui_glue.startApp()
except: 
    raise 

finally:
    pass