## Very specific, simple script for VoxCommando users.
## For context, see forum threads: 
## http://voxcommando.com/forum/index.php?topic=1948 
## http://voxcommando.com/forum/index.php?topic=1836.msg15948
####################################################################################################

import clr,time,thread
clr.AddReference("System.Management")
from System.Collections.Generic import *
from System.Management import ManagementObject


def getLoad(secs):
    while not killPy:
       mo = ManagementObject("Win32_PerfFormattedData_PerfOS_Processor.Name='_total'")
       load = mo["PercentProcessorTime"]
       #print load
       
       #load val over 10% triggers VC event. Change this as desired. Passes load% val as event payload {1}.
       if load > 10: 
          vc.triggerEvent("CPU.load", List[str]([str(load)]))
       
       #pause between loops:currently 300 secs (5 mins)
       time.sleep(secs)
       
thread.start_new_thread(getLoad, (300,))
