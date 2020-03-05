from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np


class App(QtGui.QMainWindow):
    switch_graphs = True
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)

        self.canvas = pg.GraphicsLayoutWidget()
        
        self.label = QtGui.QLabel()

        lay = QtGui.QVBoxLayout(self.mainbox)
        lay.addWidget(self.canvas)
        lay.addWidget(self.label)
        # self.mainbox.addWidget(self.canvas)

        self.img_items = []

        for i in range(1):
            for j in range(4): 
                # view = self.canvas.addViewBox()
                w = self.canvas.addPlot(row=i, col=j, title="data 1")
                # print(type(w))
                plt = w.plot([0,1,2,3] , [0,1,2,3] , clear=True)
                
                self.img_items.append(plt)

            self.canvas.nextRow()

        self.timer = QtCore.QTimer(self, interval=1000)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update)
        self.timer.start(2)

    def _update(self):

        for item in self.img_items:            
            if(self.switch_graphs): 
                self.switch_graphs = False
                # print(type(item))
                item.setData([0,1,2,3])
            else: 
                print("2")
                self.switch_graphs = True
                item.setData([3,2,1,0])
        pg.QtGui.QApplication.processEvents()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    # print("hello")
    sys.exit(app.exec_())