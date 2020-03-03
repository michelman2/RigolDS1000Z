import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation , FFMpegFileWriter
from matplotlib.axes import Axes


def create_sine(number_of_samples, time_frequency , time_length , init_phase_degree=0): 
    init_phase_radian = init_phase_degree * np.pi / (180)
    
    x = np.linspace(0 , time_length , number_of_samples)
    y = np.sin(2 * np.pi * time_frequency * x + init_phase_radian)

    return (x , y)

def mix_sines(sine_tuple_arrays , number_of_each):
    
    last_sine_x_time = 0 
    whole_frame_x = []
    whole_frame_y = []
    for _ in np.arange(number_of_each): 
        for _ , sine_tuple in enumerate(sine_tuple_arrays): 
            sine_x = sine_tuple[0]
            sine_y = sine_tuple[1]

            shifted_x = np.add(last_sine_x_time , sine_x)
            for _ , val in enumerate(shifted_x): 
                whole_frame_x.append(val)
            last_sine_x_time = shifted_x[-1]

            for _ , valy in enumerate(sine_y): 
                whole_frame_y.append(valy)

    
    return (whole_frame_x , whole_frame_y)

def find_idx_in_sorted_list(sorted_list , element): 
    for idx , val in enumerate(sorted_list): 
        if(val >= element): 
            return idx
            


def get_fft(yt_tuple , window_duration , window_start_time): 
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
    
    window_start_idx = find_idx_in_sorted_list(tuple_time , window_start_time)
    window_end_idx = find_idx_in_sorted_list(tuple_time , window_end_time)

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
    
class animatedFigure: 
    fig = None 
    ax = None
    axvline1 = None
    axvline2 = None  
    step = 0.1

    def __init__(self , xy_pair , window_start , window_duration): 
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(211)
        print(type(self.ax))
        self.xdata = xy_pair[0]
        self.ydata = xy_pair[1]
        self.xy_pair = xy_pair

        self.ln , = plt.plot(self.xdata , self.ydata)
        self.axvline1 = plt.axvline(window_start , ymin=0 , ymax=1)
        self.axvline2 = plt.axvline(window_duration + window_start , ymin=0 , ymax=1)
        
        self.window_start = window_start
        self.window_duration = window_duration
        self.ln.set_data(self.xdata , self.ydata)

        ## create second figure for fft
        self.fft_ax = self.fig.add_subplot(212)
        self.fft_line, = plt.plot([0] , [0])

    def __update_frame(self , i): 
        ## set axvlines to a new frame
        self.axvline1.set_xdata(self.window_start + i)
        self.axvline2.set_xdata(self.window_start + self.window_duration + i)

        ## get fft of the lines
        [self.fft_pair , self.time_window_pair]= get_fft(self.xy_pair, 
                                    window_start_time=self.window_start + i , 
                                    window_duration=self.window_duration)


        self.fft_ax.set_xlim(0, 20)
        self.fft_ax.set_ylim(0,1)
        self.fft_line.set_xdata(self.fft_pair[0])
        self.fft_line.set_ydata(self.fft_pair[1])


        return self.ln , self.ax

    def animate_function(self): 
        self.anim = FuncAnimation(self.fig , self.__update_frame , 
                                    frames=np.arange(0,np.max(self.xdata) - (self.window_duration),step=self.step), 
                                    interval=200)


    def set_sliding_step(self , step): 
        if(step > 0): 
            self.step = step

    def set_sliding_interval(self , slide_interval:int): 
        if(slide_interval > 0): 
            self.slide_interval = slide_interval

class animateFFT: 
    fig = None 
    ax = None
    axvline1 = None
    axvline2 = None  
    step = 0.1

    def __init__(self , xy_pair , window_start , window_duration): 
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(211)
        print(type(self.ax))
        self.xdata = xy_pair[0]
        self.ydata = xy_pair[1]
        self.xy_pair = xy_pair

        self.ln , = plt.plot(self.xdata , self.ydata)
        self.axvline1 = plt.axvline(window_start , ymin=0 , ymax=1)
        self.axvline2 = plt.axvline(window_duration + window_start , ymin=0 , ymax=1)
        
        self.window_start = window_start
        self.window_duration = window_duration
        self.ln.set_data(self.xdata , self.ydata)

        ## create second figure for fft
        self.fft_ax = self.fig.add_subplot(212)
        self.fft_line, = plt.plot([0] , [0])

    def __update_frame(self , i): 
        ## set axvlines to a new frame
        self.axvline1.set_xdata(self.window_start + i)
        self.axvline2.set_xdata(self.window_start + self.window_duration + i)

        ## get fft of the lines
        [self.fft_pair , self.time_window_pair]= get_fft(self.xy_pair, 
                                    window_start_time=self.window_start + i , 
                                    window_duration=self.window_duration)


        self.fft_ax.set_xlim(0, 20)
        self.fft_ax.set_ylim(0,1)
        self.fft_line.set_xdata(self.fft_pair[0])
        self.fft_line.set_ydata(self.fft_pair[1])


        return self.ln , self.ax

    def animate_function(self): 
        self.anim = FuncAnimation(self.fig , self.__update_frame , 
                                    frames=np.arange(0,np.max(self.xdata) - (self.window_duration),step=self.step), 
                                    interval=200)


    def set_sliding_step(self , step): 
        if(step > 0): 
            self.step = step

    def set_sliding_interval(self , slide_interval:int): 
        if(slide_interval > 0): 
            self.slide_interval = slide_interval
## start and end of the window

fft_win_start = 0
fft_win_durat = 1



getsine = create_sine(number_of_samples = 5000 ,
                        time_frequency = 1 , 
                        time_length = 2 ,
                        init_phase_degree = 40 )
getsine2 = create_sine(number_of_samples = 5000,
                        time_frequency = 5 , 
                        time_length = 2, 
                        init_phase_degree=0)



mixed_sine = mix_sines([getsine , getsine2] , 2)
[fft_pair , time_window_pair]= get_fft(mixed_sine, 
                                    window_start_time=fft_win_start , 
                                    window_duration=fft_win_durat)

## plotting the results
# plt.figure()
# plt.plot(mixed_sine[0] , mixed_sine[1])
# plt.axvline(time_window_pair[0] , 0 , 1)
# plt.axvline(time_window_pair[1] , 0 , 1)

animator = animateFFT(mixed_sine , window_start=fft_win_start,
                                                    window_duration=fft_win_durat)
animator.animate_function()

# plt.figure()
# plt.plot(fft_pair[0] , fft_pair[1])


plt.show()



