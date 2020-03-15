import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import Rigol_Lib.RigolSCPI as rs

import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp
import TCPconnection.TCPListener as tl

import threading
from Rigol_util import channelDataKeeper as cld
from Gui import controlAndProcess
import queue
import time
from TransactionMeans import LimitedQueue

class tester: 
    
    def perma_loop(self):
        
        while(True): 
            time.sleep(0.1) 
            print("h")




if __name__ == "__main__": 
    log_list = []

    myq = LimitedQueue.LimitedQueue(10)
    mylist = range(100)
    idx = 0

    process_model = controlAndProcess.ProcessModel()
    process_model.connect_f2q(process_model.rawDataRead , myq)

    loopCount = 50
    currnt_cnt = 0

    
    process_model.setProcessor(controlAndProcess.fftprocess)

    while(currnt_cnt < loopCount):
        print(currnt_cnt)
        currnt_cnt += 1 
        time.sleep(0.01)
        if(idx >= len(mylist)): 
            idx = 0 
        myq.put(mylist[idx])
        process_model.makeThread_RawDataReader()
        idx += 1

        output_queue = process_model.getOutputQueue()
        while(not output_queue.empty()): 
            try: 
                current_proc = output_queue.get_nowait()
                if(current_proc.is_process_alive()): 
                    output_queue.put(current_proc)
                else: 
                    log_list.append(current_proc.get_response())
            except: 
                
                pass 
            
            

    print(process_model.getLogData())
    print(log_list)