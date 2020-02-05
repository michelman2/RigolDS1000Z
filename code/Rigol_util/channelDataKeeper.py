class channelDataKeeper: 
    __data_value = None
    __data_idx = None
    ## The class initiates itself for a specific channel. The channel index is 
    # taken from the enum in rigol_lib
    # The class also allows subscription of different classes that implement inform method
    def __init__(self , channel_index): 
        self.__channel = channel_index
        self.__observers = []

        
    ## The data keeper object keeps data with the following format 
    # data comes in the following format: data_tuple = ([index list] , [data value list])
    def set_data(self , data_tuple): 
        if(data_tuple != None): 
            self.__data_idx = data_tuple[0]
            self.__data_value = data_tuple[1]
            self.__update_observers()

    ## set channel vertical unit spacing
    def set_channel_v_unit(self , channel_v_unit): 
        self.__channel_v_unit = channel_v_unit

    ## set channel horizontal unit spacing
    def set_channel_h_unit(self , channel_h_unit): 
        self.__channel_h_unit = channel_h_unit


    ## channel sampling rate
    def set_channel_sampling_rate(self , srate): 
        self.__sampling_rate = srate

    def subscribe(self , observer_subj): 
        self.__observers.append(observer_subj)

    def __update_observers(self):
        for observer in self.__observers: 
            # print("hello")
            observer.update(self)

    ## get channel info: 
    def get_data_value(self): 
        return self.__data_value

    def get_data_idx(self): 
        return self.__data_idx

    def get_channel_v_unit(self): 
        return self.__channel_v_unit

    def get_channel_h_unit(self): 
        return self.__channel_h_unit
    
    def get_channel_sampling_rate(self): 
        return self.__sampling_rate


    