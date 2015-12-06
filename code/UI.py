#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore 
#from PyQt4.phonon import Phonon
import pyqtgraph as pg
import numpy as np
from pyqtgraph.ptime import time
import pyqtgraph.opengl as gl



class LeftDockerWidget(QtGui.QWidget):
    def __init__(self):
        super(LeftDockerWidget, self).__init__()
        self.textEdit = QtGui.QTextEdit()
        self.initUI();
    
    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.textEdit)
        self.setLayout(vbox)
    def update_status(self,direction):
        self.textEdit.append(direction);



class RightDockerWidget(QtGui.QWidget):
    def __init__(self):
        super(RightDockerWidget, self).__init__()
        self.textEdit = QtGui.QTextEdit()
        self.plotWidget=pg.PlotWidget()
        #self.plot=self.plotWidget.plot()
        self.resize(10,10)
        self.initUI()   
    def initUI(self):
        self.plotWidget.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.textEdit)
        vbox.addWidget(self.plotWidget)
        self.setLayout(vbox)
    def update_status(self,newstatus):
        self.textEdit.append(newstatus);

    def update_plot(self,newdata):
        self.plotWidget.clear()
        if(newdata==0):
            newdata=np.random.normal(size=(20,14))
        row, column = newdata.shape
        for i in range(0,column):
            self.plotWidget.plot(newdata[:][i]+i,pen=(255-(i%5)*20,(i%6)*50,i+100),name="channel "+str(i+1))

       
class TopDockerWidget(QtGui.QWidget):
    def __init__(self):
        super(TopDockerWidget, self).__init__()
        self.connect_btn = QtGui.QPushButton('Connect', self)
        self.start_btn = QtGui.QPushButton('Start',self)
        self.initUI();
    def initUI(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.connect_btn)
        hbox.addWidget(self.start_btn)
        self.setLayout(hbox)



class Mainwindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(Mainwindow, self).__init__()      
        self.exitAction = QtGui.QAction(QtGui.QIcon('close.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)
        self.statusBar()
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.exitMenu = self.menubar.addMenu('&Exit')
        #fileMenu.addAction(exitAction1)
        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAction)
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowTitle('BCI System Nanjing University Li Meng')
        self.setWindowIcon(QtGui.QIcon('Icon_system.png'))    
        
        #---Left  Docker
        
        dockWidgetleft =QtGui.QDockWidget("Direction",self)
        dockWidgetleft.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.Leftdocker = LeftDockerWidget()
        dockWidgetleft.setWidget(self.Leftdocker)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidgetleft)
        
        #---Right Docker
        dockWidgetright =QtGui.QDockWidget("Status",self)
        dockWidgetright.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.Rightdocker = RightDockerWidget()
        dockWidgetright.setWidget(self.Rightdocker)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidgetright)
        
        #---Top Docker
        dockWidgettop =QtGui.QDockWidget("Tool",self)
        dockWidgettop.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.Topdocker = TopDockerWidget()
        dockWidgettop.setWidget(self.Topdocker)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dockWidgettop)

        w = gl.GLViewWidget()
        #w.resize(6,800)
        w.opts['distance'] = 200
        w.setWindowTitle('pyqtgraph example: GLImageItem')

        ## create volume data set to slice three images from
        shape = (100,100,70)
        data = pg.gaussianFilter(np.random.normal(size=shape), (4,4,4))
        data += pg.gaussianFilter(np.random.normal(size=shape), (15,15,15))*15

        ## slice out three planes, convert to RGBA for OpenGL texture
        levels = (-0.08, 0.08)
        tex1 = pg.makeRGBA(data[shape[0]/2], levels=levels)[0]       # yz plane
        tex2 = pg.makeRGBA(data[:,shape[1]/2], levels=levels)[0]     # xz plane
        tex3 = pg.makeRGBA(data[:,:,shape[2]/2], levels=levels)[0]   # xy plane

        v1 = gl.GLImageItem(tex1)
        v1.translate(-shape[1]/2, -shape[2]/2, 0)
        v1.rotate(90, 0,0,1)
        v1.rotate(-90, 0,1,0)
        w.addItem(v1)
        v2 = gl.GLImageItem(tex2)
        v2.translate(-shape[0]/2, -shape[2]/2, 0)
        v2.rotate(-90, 1,0,0)
        w.addItem(v2)
        v3 = gl.GLImageItem(tex3)
        v3.translate(-shape[0]/2, -shape[1]/2, 0)
        w.addItem(v3)
        ax = gl.GLAxisItem()
        w.addItem(ax)
        self.setCentralWidget(w);
        self.resize(1200,500)
    
