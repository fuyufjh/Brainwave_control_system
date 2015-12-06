#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore 
from Bcisystem import *

def main():
	app = QtGui.QApplication(sys.argv)
	mian_system= Bcisystem()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
