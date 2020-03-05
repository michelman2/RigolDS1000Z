from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import random
import numpy as np

import time

import threading



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.central_widget.addWidget(self.login_widget)

    def plotter(self):
        self.data =[0]
        
        # self.curve = self.login_widget.plot.getPlotItem().plot()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)

    def updater(self):
        # self.data.append(self.data[-1]+0.2*(0.5-random.random()) )
        self.data = np.random.randint(low=1, high=100, size=2000)
        self.x = np.linspace(0 , 100 , len(self.data))
        curves = self.login_widget.getCurves()
        for i in range(4): 
            # print(type(curves[i]))
            # curves[i].setData(self.data)
            curves[i].setData(self.x , self.data)


        # self.curve.setData(self.data)

class LoginWidget(QtGui.QWidget):
    plot_list1 = []
    plot_list2 = []

    plot_curves = []

    def getCurves(self): 
        return self.plot_curves

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.col1 = QtGui.QVBoxLayout()
        self.col2 = QtGui.QVBoxLayout()
        self.control_column = QtGui.QVBoxLayout()

        self.main_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.control_column)
        self.main_panel.addLayout(self.col1)
        self.main_panel.addLayout(self.col2)

        self.button = QtGui.QPushButton('Start Plotting')
        self.control_column.addWidget(self.button)

        current_layout = self.col1
        plotlist = self.plot_list1

        for i in range(2): 
            for j in range(4): 
                plotter = pg.PlotWidget()
                current_layout.addWidget(plotter)
                plotlist.append(plotter)
                self.plot_curves.append(plotter.getPlotItem().plot())
            current_layout = self.col2
            plotlist = self.plot_list2

        # self.plot = pg.PlotWidget()
        # layout.addWidget(self.plot)
        # layout.addWidget(self.plot)
        self.setLayout(self.main_panel)



if __name__ == '__main__':
    
    printth = threading.Thread(target=print_in_thread,args=())
    printth.daemon = True 
    printth.start()

    

    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


    