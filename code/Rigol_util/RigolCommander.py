
import Rigol_Lib.RigolSCPI as rscpi
import TCPconnection.MessageIterables as mi


class RigolCommander: 
    """
        holds wrapper methods to alleviate generation of commands for oscilloscope
        getting commands by a behaviour
    """

    def __init__(self):
        self.scpi_lib = rscpi.RigolSCPI()


    def initalize_data_query_byte(self , chann): 
        """
            initializing oscilloscope to: 
                1) get device id 
                2) running device
                3) set waveform source to a channel
                4) set waveform mod 
                5) set waveform return mode 
        """
        message_list = []
        message_list.append(self.scpi_lib.identify_device())
        message_list.append(self.scpi_lib.run())
        message_list.append(self.scpi_lib.set_waveform_source(chann))
        message_list.append(self.scpi_lib.set_waveform_mode(rscpi.RIGOL_WAVEFORM_MODE.NORMAL))
        message_list.append(self.scpi_lib.set_waveform_format(rscpi.RIGOL_WAVEFORM_FORMAT.BYTE)) 
        return self.__wrap_in_message_holder(message_list)
     
    def ask_oscilloscope_for_data(self): 
        """
            Queries data from oscilloscope
        """
        message_list = []
        message_list.append(self.scpi_lib.query_waveform_data())
        return self.__wrap_in_message_holder(message_list)

    # def get_status_registers(self): 


    def __wrap_in_message_holder(self , message_list): 
        message_holder = mi.IterMessageList(message_list)
        return message_holder