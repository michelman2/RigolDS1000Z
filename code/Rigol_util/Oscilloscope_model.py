from Rigol_Lib import RigolSCPI

class Oscilloscope: 
    __channel_x_increments = [None , None , None , None]
    __channel_y_increments = [None , None , None , None]

    __current_active_channel = None 

    __oscilloscope_available_ch = []

    def __init__(self , avaialable_ch:list): 
        self.__oscilloscope_available_ch = avaialable_ch
        pass


    def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX):
        self.__current_active_channel = channel

    def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        return self.__current_active_channel


    def get_channel_x_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
        return self.__channel_x_increments[channel.get_data_val()]

    def get_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
        return self.__channel_y_increments[channel.get_data_val()]

    def set_channel_x_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , x_inc:float): 
        self.__channel_x_increments[channel] = x_inc

    def set_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , y_inc:float): 
        self.__channel_y_increments[channel] = y_inc

    def get_next_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        if(self.__current_active_channel == None or len(self.__oscilloscope_available_ch)==0): 
            return None

        else: 
            current_idx = self.__oscilloscope_available_ch.index(self.__current_active_channel)
            next_idx = current_idx + 1
            if(next_idx >= len(self.__oscilloscope_available_ch)): 
                next_idx = 0 
            return self.__oscilloscope_available_ch[next_idx]
