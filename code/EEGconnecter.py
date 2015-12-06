# python version >= 2.5
import ctypes
import sys
import os
from ctypes import *
from numpy import *
import time
from ctypes.util import find_library
from Bcicache import *


#---------------------
class connect_emotiv():
    def __init__(self):
        self.cache = cache()
        self.libEDK = cdll.LoadLibrary("edk.dll")
        self.ED_COUNTER = 0
        self.ED_INTERPOLATED=1
        self.ED_RAW_CQ=2
        self.ED_AF3=3
        self.ED_F7=4
        self.ED_F3=5
        self.ED_FC5=6
        self.ED_T7=7
        self.ED_P7=8
        self.ED_O1=9
        self.ED_O2=10
        self.ED_P8=11
        self.ED_T8=12
        self.ED_FC6=13
        self.ED_F4=14
        self.ED_F8=15
        self.ED_AF4=16
        self.ED_GYROX=17
        self.ED_GYROY=18
        self.ED_TIMESTAMP=19
        self.ED_ES_TIMESTAMP=20
        self.ED_FUNC_ID=21
        self.ED_FUNC_VALUE=22
        self.ED_MARKER=23
        self.ED_SYNC_SIGNAL=24
        #         IN DLL(edk.dll)
        #         typedef enum EE_DataChannels_enum {
        #            ED_COUNTER = 0, ED_INTERPOLATED, ED_RAW_CQ,
        #            ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,
        #            ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,
        #            ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX,
        #            ED_GYROY, ED_TIMESTAMP, ED_ES_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER,
        #            ED_SYNC_SIGNAL
        #         } EE_DataChannel_t;
        self.targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
        self.header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
        self.write = sys.stdout.write
        self.eEvent     = self.libEDK.EE_EmoEngineEventCreate()
        self.eState     = self.libEDK.EE_EmoStateCreate()
        self.userID     = c_uint(0)
        self.nSamples   = c_uint(0)
        self.nSam       = c_uint(0)
        self.nSamplesTaken  = pointer(nSamples)
        self.da = zeros(128,double)
        self.data     = pointer(c_double(0))
        self.user     = pointer(userID)
        self.composerPort  = c_uint(1726)
        self.secs      = c_float(1)
        self.datarate  = c_uint(0)
        self.readytocollect = False
        self.option      = c_int(0)
        self.state     = c_int(0)
    def connect(self):
        #if option == 1:
        print self.libEDK.EE_EngineConnect("Emotiv Systems-5")
        if self.libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
            print "Emotiv Engine start up failed."
            return 0
        #elif option == 2:
        if self.libEDK.EE_EngineRemoteConnect("127.0.0.1", self.composerPort) != 0:
            print "Cannot connect to EmoComposer on"
            return 0
        #else :print "option = ?"
        print "success connect to the Emotiv"
        return 1


    def getdata(self):
        print "Start receiving EEG Data! Press any key to stop logging...\n"
        self.f = file('EEG.csv', 'w')
        self.f = open('EEG.csv', 'w')
        print >> self.f,self.header
        hData = self.libEDK.EE_DataCreate()
        self.libEDK.EE_DataSetBufferSizeInSec(secs)
        print "Buffer size in secs:"
        while (1):
            state = self.libEDK.EE_EngineGetNextEvent(eEvent)
            if state == 0:
                eventType = self.libEDK.EE_EmoEngineEventGetType(eEvent)
                self.libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
            if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
                print "User added"
                self.libEDK.EE_DataAcquisitionEnable(self.userID,True)
                self.readytocollect = True
            if self.readytocollect==True:
                self.libEDK.EE_DataUpdateHandle(0, hData)
                self.libEDK.EE_DataGetNumberOfSample(hData,self.nSamplesTaken)
                print "Updated :",self.nSamplesTaken[0]
            if self.nSamplesTaken[0] != 0:
                self.nSam=self.nSamplesTaken[0]
                arr=(ctypes.c_double*self.nSamplesTaken[0])()
                ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
                #libEDK.EE_DataGet(hData, 3,byref(arr), nSam)
                self.data = array('d')#zeros(nSamplesTaken[0],double)
                sampledata=[]
            for sampleIdx in range(self.nSamplesTaken[0]):
                for i in range(1,15):
                    self.libEDK.EE_DataGet(hData,self.targetChannelList[i],byref(arr), self.nSam)
                    sampledata.append(arr[sampleIdx])
                    print >>f,arr[sampleIdx],",",
                self.cache.write_catche(sampledata);
                sampledata=[]
                print >>f,'\n'
        time.sleep(0.2)
        self.libEDK.EE_DataFree(hData)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.libEDK.EE_EngineDisconnect()
        self.libEDK.EE_EmoStateFree(self.eState)
        self.libEDK.EE_EmoEngineEventFree(self.eEvent)