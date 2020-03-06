# import from Rigol_Lib import RigolSCPI

# class Oscilloscope: 
#     __channel_x_increments = [None , None , None , None]
#     __channel_y_increments = [None , None , None , None]

#     __current_active_channel = None 

#     def __init__(self): 
        
#         pass


#     def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX):
#         self.__current_active_channel = channel

#     def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
#         return self.__current_active_channel


#     def get_channel_x_increment(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX)->float: 
#         return self.__channel_x_increments[channel.get_data_val]

#     def get_channel_y_increment(self , channel:RigolSCPI.rigol)
