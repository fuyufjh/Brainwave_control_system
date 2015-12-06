#Report

# System Architecture

```
sequenceDiagram
    loop system on 
    User->>BCI System: Brain Wave Data(128HZ)
    BCI System->>Robert: Control Code
    Robert->>User: Camera snapshot
    end
```
----
#BCI system
```
 graph TB
         subgraph 1 Receive Data Module 
         id11[Bluetooth Receiver]-->id12[Memory]
         id12[Memory] -->id21[Filter data]
         end
        
         subgraph 2 PreProcessing
         id21[Fileter]-->id22[Normalization]
         id22-->id31[Recongnize]
         end
         
         
         subgraph 3 Classify
         id31[Recongnize]-->id41
         end
         
         
         subgraph 4 Control Module
         id41[Robert Control and Camera]
         id41-->id31
         end    
```
Library Dependency  
    1.numpy    
    2.pyqt   
    3.pyqtgraph   
    4.opengl  
    5.sklearn    

#Work finished

 1.The Bci software 
 2.Data set est
 3.Classifer test
 

#Work unfinished

 1. Robort car control module
 2. Camera connect module



