from Rigol_Lib import RigolSCPI
from TCPconnection import MessageIterables


class Oscilloscope: 
    
    __x_increments = 1 
    __channel_y_increments = [1 , 1 , 1 , 1]
    __channel_y_offset = [0,0,0,0]
    __x_orig = 0 

    __current_active_channel = None 

    __oscilloscope_available_ch = []

    def __init__(self , avaialable_ch:list): 
        self.__oscilloscope_available_ch = avaialable_ch
        pass


    def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX):
        self.__current_active_channel = channel

    def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        return self.__current_active_channel


    def get_x_increment(self)->float: 
        return self.__x_increments

    def get_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
        answer = self.__channel_y_increments[channel.get_data_val()]
        return answer

    def set_channel_x_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , x_inc:float): 
        self.__x_increments = x_inc

    def set_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , y_inc:float): 
        
        self.__channel_y_increments[channel.get_data_val()] = y_inc

    def __set_channel_y_offset(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , y_offset:float): 
        self.__channel_y_offset[channel.get_data_val()] = y_offset
    
    def __set_x_orig(self , x_orig:float): 
        self.__x_orig = x_orig

    def get_channel_y_offset(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
        return self.__channel_y_offset[channel.get_data_val()]

    def get_x_orig(self)->float: 
        return self.__x_orig

    def get_next_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        if(self.__current_active_channel == None or len(self.__oscilloscope_available_ch)==0): 
            return None

        else: 
            current_idx = self.__oscilloscope_available_ch.index(self.__current_active_channel)
            next_idx = current_idx + 1
            if(next_idx >= len(self.__oscilloscope_available_ch)): 
                next_idx = 0 
            return self.__oscilloscope_available_ch[next_idx]

    def get_channels_iterable(self): 
        ch_list = self.__oscilloscope_available_ch
        return MessageIterables.IterMessageList(ch_list, resettable=True)

    def update_preamble(self , command:RigolSCPI.cmdObj):
        """
            Updates only the acquired dimension variables of the oscilloscope
            No changes should be done to active channel, as the channel in the command
            argument is from a past state 
        """
        if(command.get_parser().get_response_type() != RigolSCPI.SCPI_RESPONSE_TYPE.PREAMBLE): 
            raise WRONG_ARG_TYPE
        
        cmd_channel = command.get_active_channel()
        preamb = command.get_parser().get_preamble()
        
        ## response format (discarded)
        oscill_format = preamb[0]
        oscill_type = preamb[1]
        points_count = preamb[2]
        average_window = preamb[3]
        xinc = preamb[4]
        xorigin = preamb[5]
        xreference = preamb[6]
        yinc = preamb[7]
        yorigin = preamb[8]
        yrefernce = preamb[9]

        self.set_channel_x_increment(channel=cmd_channel , x_inc=xinc)
        self.set_channel_y_increment(channel=cmd_channel , y_inc=yinc)
        # self.__set_x_orig(xorigin)
        self.__set_channel_y_offset(channel=cmd_channel , y_offset=yrefernce)
        




class WRONG_ARG_TYPE(Exception): 
    pass