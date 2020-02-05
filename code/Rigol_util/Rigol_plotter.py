from matplotlib import pyplot as plt
import threading
import matplotlib


class RigolPlotter: 
    
    __channel_data_keepers = []
    __update_flag = False  
    # __lock = threading.Lock()

    def __init__(self): 
        pass 
        

    def add_channel_data_keeper(self , data_keeper_obj):         
        data_keeper_obj.subscribe(self)
        self.__channel_data_keepers.append(data_keeper_obj)

    ## update is called by channelDataKeeper object when a new reading 
    # is saved. If the update flag is set, the plot is redrawn 
    def update(self, caller):
        # with self.__lock: 
        self.__data_idx = caller.get_data_idx()
        self.__data_value = caller.get_data_value()
        self.__update_flag = True
            
    ## plot data
    # update the plots 
    def update_plot(self): 
        self.__fig , self.__ax = plt.subplots() 
        # plt.ion()
        # self.__fig = plt.figure()
        # self.__ax = plt.subplot(1,1,1)
        # print("a")
        while(True):            
            # with self.__lock:
            # plt.pause(0.001) 
            # plt.gcf().canvas.draw_idle()
            # plt.gcf().canvas.start_event_loop(0.0001)
            # print(self.__update_flag)

            if(self.__update_flag): 
                # print(self.__update_flag)
                # self.__update_flag = False
                # self.__ax.plot(self.__data_idx , self.__data_value)
                # plt.draw()
                # plt.pause(0.001)
                plt.plot(self.__data_idx , self.__data_value)
                # plt.gcf().canvas.draw_idle()
                # plt.gcf().canvas.start_event_loop(0.0001)
                    

        
    
    
