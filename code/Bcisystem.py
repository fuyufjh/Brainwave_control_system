#!/usr/bin/python
# -*- coding: utf-8 -*-
import thread
import time
import numpy as np
from UI import *
from EEGconnecter import *
from Bcicache import *
from Bciclassifier import *
from Bcicontrolcode import *
from EEGconnecter import *


class Bcisystem:
	def __init__(self):
		self.connected = 0;
		#self.connecter = connect_emotiv()
		self.classfier = Bciclassifier()
		self.controlcode = Bcicontrolcode()
		self.ui = Mainwindow()
		#self.ui.Topdocker.connect_btn.clicked.connect(self.systemconnect())
		self.ui.Topdocker.start_btn.clicked.connect(self.systemstart)
		self.ui.show()

	def systemconnect(self):
		if(self.connecter.connect()==1):
			self.connected = 1
			self.ui.Rightdocker.textEdit.append("Succeed to connect too the Emotiv")
		else:
			self.ui.Rightdocker.textEdit.append("Failed to connect to the Emotiv")

	def systemstart(self):
		if(self.connected==0):
			self.ui.Rightdocker.textEdit.append("Failed to start, unable to conenct to the Emotiv")
			self.ui.Rightdocker.update_plot(0)
		else:
			self.ui.Rightdocker.textEdit.append("Succeed to connect to the Emotiv")
		try:
   			thread.start_new_thread(self.connecter.getdata,())
   			#thread.start_new_thread(self.run_machine,())
		except:
			self.ui.Rightdocker.textEdit.append("Error: unable to start thread")
			self.ui.Leftdocker.textEdit.append("Directions undetected ")
		self.run_machine()
			
	def run_machine(self):
		#while(1):
			#self.ui.Rightdocker.textEdit.append("Thread running")	
			#time.sleep(5)
		while(1):
			data = np.asarray(self.connecter.cache.getalldata())
			self.ui.Rightdocker.update_plot(data)
			label = self.classfier.predict(data)
			directions=self.controlcode.directions(label)
			for i in directions:
				self.ui.Leftdocker.textEdit.append("Directions detected "+i)
			#All ends here for the bci system









			





	



    

		



		


