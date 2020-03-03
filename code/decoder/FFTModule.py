import threading 
from threading import Lock
import numpy as np


fft_lock = Lock()


class FFTModule: 

    def __init__(self): 
        pass


    def find_idx_in_sorted_list(self, sorted_list , element): 
        for idx , val in enumerate(sorted_list): 
            if(val >= element): 
                return idx


    def get_fft(self , yt_tuple , window_duration , window_start_time): 
        ## extract fft values
        tuple_time = yt_tuple[0]
        tuple_val = yt_tuple[1]

        ## in order for the window to fall completely inside data samples the start is adjusted if it overflows
        
        if(window_start_time > tuple_time[-1] - window_duration): 
            window_start_time = tuple_time[-1] - window_duration
            

        ## TODO: handle error 
        if(window_start_time < 0): 
            return -1
            
        
        ## window's unit is in seconds (or time unit), to extract data we need to find the index
        window_end_time = window_start_time + window_duration
        
        window_start_idx = self.find_idx_in_sorted_list(tuple_time , window_start_time)
        window_end_idx = self.find_idx_in_sorted_list(tuple_time , window_end_time)

        windowed_time = tuple_time[window_start_idx:window_end_idx]
        windowed_val = tuple_val[window_start_idx:window_end_idx]
   

        N = np.array(windowed_time).size
        T = windowed_time[1] - windowed_time[0]

        if(T == 0): 
            T = windowed_time[2] - windowed_time[1]
        
        freq = np.linspace(0 , 1/T , N)
        fft = np.fft.fft(windowed_val)

        ## the return value is as follows: 
        ## [(fft x , fft y) , (fft win start time , fft win end time)]
        return [(freq[:N//2] , np.abs(fft[:N//2])*(1/N)) , (windowed_time[0] , windowed_time[-1])]
        