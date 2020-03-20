from Rigol_Lib import RigolSCPI
from TCPconnection import MessageIterables
import numpy as np

# class Oscilloscope: 

#     def __init__(self , active_channels:list , total_channel_cnt=0): 
#         if(total_channel_cnt == 0):
#             ## default number of channels in oscilloscope in case 
#             ## it is not provided 
#             self.__total_channel_cnt = 4
#         else: 
#             self.__total_channel_cnt = total_channel_cnt

#         self.__active_channels = active_channels
#         self.__x_increments = 1 
#         self.__channel_y_increments = [1 for _ in range(self.__total_channel_cnt)]
#         self.__channel_y_offset = [0 for _ in range(self.__total_channel_cnt)]
#         self.__x_orig = 0 
#         self.__current_active_channel = None 

#     def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX):
#         self.__current_active_channel = channel

#     def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
#         return self.__current_active_channel

#     def get_channel_cnt(self)->int: 
#         return self.__total_channel_cnt

#     def get_x_increment(self)->float: 
#         return self.__x_increments

#     def get_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
#         answer = self.__channel_y_increments[channel.get_data_val()]
#         return answer

#     def set_channel_x_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , x_inc:float): 
#         self.__x_increments = x_inc

#     def set_channel_y_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , y_inc:float): 
        
#         self.__channel_y_increments[channel.get_data_val()] = y_inc

#     def __set_channel_y_offset(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX , y_offset:float): 
#         self.__channel_y_offset[channel.get_data_val()] = y_offset
    
#     def __set_x_orig(self , x_orig:float): 
#         self.__x_orig = x_orig

#     def get_channel_y_offset(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
#         return self.__channel_y_offset[channel.get_data_val()]

#     def get_x_orig(self)->float: 
#         return self.__x_orig

#     def get_next_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
#         if(self.__current_active_channel == None or len(self.__active_channels)==0): 
#             return None

#         else: 
#             current_idx = self.__active_channels.index(self.__current_active_channel)
#             next_idx = current_idx + 1
#             if(next_idx >= len(self.__active_channels)): 
#                 next_idx = 0 
#             return self.__active_channels[next_idx]

#     def get_channels_iterable(self): 
#         ch_list = self.__active_channels
#         return MessageIterables.IterMessageList(ch_list, resettable=True)

#     def update_preamble(self , command:RigolSCPI.cmdObj):
#         """
#             Updates only the acquired dimension variables of the oscilloscope
#             No changes should be done to active channel, as the channel in the command
#             argument is from a past state 
#         """
#         if(command.get_parser().get_response_type() != RigolSCPI.SCPI_RESPONSE_TYPE.PREAMBLE): 
#             raise WRONG_ARG_TYPE
        
#         cmd_channel = command.get_active_channel()
#         preamb = command.get_parser().get_preamble()
        
#         ## response format (discarded)
#         oscill_format = preamb[0]
#         oscill_type = preamb[1]
#         points_count = preamb[2]
#         average_window = preamb[3]
#         xinc = preamb[4]
#         xorigin = preamb[5]
#         xreference = preamb[6]
#         yinc = preamb[7]
#         yorigin = preamb[8]
#         yrefernce = preamb[9]

#         self.set_channel_x_increment(channel=cmd_channel , x_inc=xinc)
#         self.set_channel_y_increment(channel=cmd_channel , y_inc=yinc)
#         # self.__set_x_orig(xorigin)
#         self.__set_channel_y_offset(channel=cmd_channel , y_offset=yrefernce)
        

class Oscilloscope: 

    def __init__(self , available_channels:list , active_channels:list): 
        if(len(available_channels) == 0): 
            raise OscillNoChannelsFound

        for channel in active_channels: 
            if(not channel in available_channels): 
                raise WrongChannelName
        
        self.__total_channel_cnt = len(available_channels)
        self.__available_channels = available_channels
        self.__active_channels = active_channels
        self.__x_increments = 1 
        self.__channel_y_increments = [1 for _ in range(len(self.__available_channels))]
        self.__channel_y_offset = [0 for _ in range(len(self.__available_channels))]
        self.__x_orig = 0 
        self.__current_active_channel = None 

    def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX):
        self.__current_active_channel = channel

    def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        return self.__current_active_channel

    def get_channel_cnt(self)->int: 
        return self.__total_channel_cnt

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
        if(self.__current_active_channel == None or len(self.__active_channels)==0): 
            return None

        else: 
            current_idx = self.__active_channels.index(self.__current_active_channel)
            next_idx = current_idx + 1
            if(next_idx >= len(self.__active_channels)): 
                next_idx = 0 
            return self.__active_channels[next_idx]

    def get_channel_list(self)->list: 
        return self.__available_channels

    def get_active_channels_iterable(self): 
        ch_list = self.__active_channels
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
        

class OscillNoChannelsFound(Exception): 
    pass

class WrongChannelName(Exception): 
    pass

class WRONG_ARG_TYPE(Exception): 
    pass