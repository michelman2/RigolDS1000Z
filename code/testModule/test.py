
import Rigol_Lib.RigolSCPI as rs
import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp
import TCPconnection.TCPListener as tl
import time 
import threading
from matplotlib import pyplot as plt

scpi_lib = rs.RigolSCPI()

message_list = [] 

message_list.append(scpi_lib.identify_device())
message_list.append(scpi_lib.run())
message_list.append(scpi_lib.set_waveform_source(rs.RIGOL_CHANNEL_IDX.CH4))
message_list.append(scpi_lib.set_waveform_mode(rs.RIGOL_WAVEFORM_MODE.NORMAL))
message_list.append(scpi_lib.set_waveform_format(rs.RIGOL_WAVEFORM_FORMAT.BYTE))
message_list.append(scpi_lib.query_waveform_data())

# message_list.append(scpi_lib.query_acquire_averages())
# message_list.append(scpi_lib.query_channel_coupling(rs.RIGOL_CHANNEL_IDX.CH4))
# message_list.append(scpi_lib.query_channel_scale(rs.RIGOL_CHANNEL_IDX.CH4))
# message_list.append(scpi_lib.query_sampling_rate())

# message_list.append(scpi_lib.identify_device())


## message list holder object
# message_holder = mi.IterMessageStack(message_list)
message_holder = mi.IterMessageList(message_list)

## Setting up tcp communication port
tcp_obj = tcp.TCPcomm()

## establishing connections
tcp_obj.establish_conn()

## Setting up a tcp listener 
tcp_listener = tl.TCPListener(tcp_obj)

## Send a message tcp
tcp_obj.send_mesage(message_holder)

## Run a thread to check tcp receiver buffer
t = threading.Thread(target=tcp_obj.read_buffer)
t.daemon = True
t.start()

oscill_data = []
oscill_data_index = []

## get data from tcp listener
try: 
    while(True): 
        data = tcp_listener.get_first_in_queue()
        if(data != None): 
            oscill_data_index = []
            oscill_data = []
            print("start_data print")
            print(len(data))
            for i in range(0 , len(data)): 
                # print("{} : {:02x}".format(i , data[i]))
                oscill_data.append(data[i])
                oscill_data_index.append(i)

            plt.figure()
            plt.plot(oscill_data_index , oscill_data)
            plt.show()
            # data2 = data[:-1]
            # data2.decode()
            # print(data)
            # d = str(data.decode()).split('\\n')
            # for instance in d:                 
            #     print(instance) 
            # print(data.decode())

            # for i in range(0 , len(data)): 
            #     oscill_data.append(data[i])

            # plt.plot(range(0 , len(data)) , data)
            # plt.show()

except KeyboardInterrupt: 
    tcp_obj.close_conn()
    exit()
