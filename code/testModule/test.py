
import Rigol_Lib.RigolSCPI as rs
import TCPconnection.MessageIterables as mi
import TCPconnection.TCPcomm as tcp


scpi_lib = rs.RigolSCPI()

message_list = [] 

message_list.append(scpi_lib.identify_device())

# message_list.append(scpi_lib.set_waveform_source(rs.RIGOL_CHANNEL_IDX.CH4))
# message_list.append(scpi_lib.set_waveform_mode(rs.RIGOL_WAVEFORM_MODE.RAW))
# message_list.append(scpi_lib.set_waveform_format(rs.RIGOL_WAVEFORM_FORMAT.BYTE))
# message_list.append(scpi_lib.query_waveform_data())

message_list.append(scpi_lib.identify_device())
# message_list.append(scpi_lib.query_acquire_type())


message_holder = mi.IterMessageStack(message_list)

connection = tcp.TCPcomm()
connection.run(message_holder)



