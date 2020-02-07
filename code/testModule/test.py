import add_path
add_path.add_subfolder_to_path("D:\\Academic\\General purpose\\communication stack\\rigol\\code")

import Rigol_Lib.RigolSCPI as rs
import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp
import TCPconnection.TCPListener as tl
import time 
import threading
from matplotlib import pyplot as plt
from Rigol_util import RigolRespProc as rrp
from Rigol_util import channelDataKeeper as cld
from Rigol_util import Rigol_plotter as rigplot



if __name__ == "__main__": 
    scpi_lib = rs.RigolSCPI()

    message_list = [] 

    message_list.append(scpi_lib.identify_device())
    message_list.append(scpi_lib.run())
    message_list.append(scpi_lib.set_waveform_source(rs.RIGOL_CHANNEL_IDX.CH4))
    message_list.append(scpi_lib.set_waveform_mode(rs.RIGOL_WAVEFORM_MODE.NORMAL))
    message_list.append(scpi_lib.set_waveform_format(rs.RIGOL_WAVEFORM_FORMAT.BYTE))
    message_list.append(scpi_lib.query_waveform_data())

    ## Add messages to a message holder 
    message_holder = mi.IterMessageList(message_list)

    ## Setting up tcp communication port
    tcp_obj = tcp.TCPcomm()

    ## establishing connections
    tcp_obj.establish_conn()

    ## Setting up a tcp listener 
    tcp_listener = tl.TCPListener(tcp_obj)

    ## Send a message tcp
    tcp_obj.send_mesage(message_holder)


    ## data holder object
    ch4_dataholder = cld.channelDataKeeper(rs.RIGOL_CHANNEL_IDX.CH4)
    
    
    t = threading.Thread(target = tcp_obj.read_buffer)
    t.daemon = True
    t.start()

    ## get data from tcp listener
    try: 
        while(True): 
            data = tcp_listener.get_first_in_queue()
            # print(data)
            if(data != None): 
                oscill_data_index = []
                oscill_data = []
                rigol_resp = rrp.RigolRespProc(data)
                
                extracted_data = rigol_resp.getHeader()
                ch4_dataholder.set_data(extracted_data)

                # tcp_obj.send_mesage(recurr_mi)
                data_ind = ch4_dataholder.get_data_idx()
                data_val = ch4_dataholder.get_data_value()
                
                if(data_ind != None and data_val != None): 
                    plt.plot(data_ind , data_val)
                    plt.show()
                # print("a")
    except KeyboardInterrupt: 
        tcp_obj.close_conn()
        exit()
