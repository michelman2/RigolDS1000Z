
import Rigol_Lib.RigolSCPI as rscpi
import TCPconnection.MessageIterables as mi




class RigolCommander: 

    def __init__(self):
        self.scpi_lib = rscpi.RigolSCPI()


    def initalize_data_query_byte(self , chann): 
        message_list = []
        message_list.append(self.scpi_lib.identify_device())
        message_list.append(self.scpi_lib.run())
        message_list.append(self.scpi_lib.set_waveform_source(chann))
        message_list.append(self.scpi_lib.set_waveform_mode(rscpi.RIGOL_WAVEFORM_MODE.NORMAL))
        message_list.append(self.scpi_lib.set_waveform_format(rscpi.RIGOL_WAVEFORM_FORMAT.BYTE)) 
        return self.__wrap_in_message_holder(message_list)
     
    def ask_oscilloscope_for_data(self): 
        message_list = []
        message_list.append(self.scpi_lib.query_waveform_data())
        return self.__wrap_in_message_holder(message_list)


    def __wrap_in_message_holder(self , message_list): 
        message_holder = mi.IterMessageList(message_list)
        return message_holder