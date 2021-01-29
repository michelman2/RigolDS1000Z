
import Rigol_Lib.RigolSCPI as rscpi
import TransactionMeans.MessageCarrier as mi

""" 
class rigol commander has the following responsibilities: 
    1) creating rigol commands in a proper format (a cmdObj in a List)
    2) Keeping the status of oscilloscope (last active channel)
    3) Parsing commands
"""
class RigolCommander: 
    """
        holds wrapper methods to alleviate generation of commands for oscilloscope
        getting commands by a behaviour
    """

    __last_active_chanel = None

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
        self.__last_active_chanel = chann
        # message_list.append(self.scpi_lib.identify_device())
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

        message_list[-1].get_parser().set_response_type(rscpi.SCPI_RESPONSE_TYPE.DATA_PAIR)
        message_list[-1].set_active_channel(self.__last_active_chanel)

        return self.__wrap_in_message_holder(message_list)

    def ask_for_preamble(self , chann): 
        message_list = []
        self.__last_active_chanel = chann
        message_list.append(self.scpi_lib.set_waveform_source(chann))

        message_list.append(self.scpi_lib.query_waveform_preamble())
        message_list[-1].get_parser().set_response_type(rscpi.SCPI_RESPONSE_TYPE.PREAMBLE)
        message_list[-1].set_active_channel(self.__last_active_chanel)

        return self.__wrap_in_message_holder(message_list)

    def ask_for_active_channel(self): 
        """ 
            queries the active channel of oscilloscope
        """
        message_list = []
        message_list.append(self.scpi_lib.query_waveform_source())
        return self.__wrap_in_message_holder(message_list)

    def __wrap_in_message_holder(self , message_list): 
        message_holder = mi.IterMessageList(message_list)
        return message_holder