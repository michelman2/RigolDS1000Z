class channelDataKeeper:
    """ 
        Holds information from one specific channel of oscilloscope. 

        The class is subscribable and can update information of observers
    """


    __data_value = None
    __data_idx = None
    
    def __init__(self , channel_index): 
        """
            channel index is an entry from list of channels available for the 
            oscilloscope.
        """

        self.__channel = channel_index
        self.__observers = []

        
    
    def set_data(self , data_tuple:tuple):
        """ 
            sets data of the channel
            data is in form of (data_idx , data_val)

        """ 
        if(data_tuple != None): 
            self.__data_idx = data_tuple[0]
            self.__data_value = data_tuple[1]
            self.__update_observers()

    
    def set_channel_v_unit(self , channel_v_unit:float):
        """
            sets vertical unit of the channel
            channel_v_unit: the ratio of channel unit to volts
                ex: 
                    mv -> channel_v_unit  = 0.001
        """ 
        self.__channel_v_unit = channel_v_unit

    
    def set_channel_h_unit(self , channel_h_unit:float): 
        """ 
            sets channel horizontal spacing (timebase)
        """
        self.__channel_h_unit = channel_h_unit


   
    def set_channel_sampling_rate(self , srate:float): 
        """
            sets channel sampling rate
        """
        self.__sampling_rate = srate

    def subscribe(self , observer_subj): 
        """
            subscribes observers
        """
        self.__observers.append(observer_subj)

    def __update_observers(self):
        """
            informs observers on any update
        """
        for observer in self.__observers: 
            # print("hello")
            observer.update(self)

    ## get channel info: 
    def get_data_value(self)->list: 
        """ 
            returns data value
            data value is a list of one snapshot
        """
        return self.__data_value

    def get_data_idx(self)->list: 
        """ 
            returns index of data values
        """
        return self.__data_idx

    def get_channel_v_unit(self)->float: 
        """ 
            returns channel vertical unit 
        """
        return self.__channel_v_unit

    def get_channel_h_unit(self)->float:
        """
            returns channel horizontal unit 
        """ 
        return self.__channel_h_unit
    
    def get_channel_sampling_rate(self)->float: 
        """
            returns sampling rate of the channel
        """
        return self.__sampling_rate


    