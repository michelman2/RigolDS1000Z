import numpy as np
from matplotlib import pyplot as plt


def create_sine(number_of_samples, time_frequency , time_length , init_phase_degree=0): 
    init_phase_radian = init_phase_degree * np.pi / (180)
    
    x = np.linspace(0 , time_length , number_of_samples)
    y = np.sin(2 * np.pi * time_frequency * x + init_phase_radian)

    return (x , y)

def mix_sines(sine_tuple_arrays , number_of_each):
    
    last_sine_x_time = 0 
    whole_frame_x = []
    whole_frame_y = []
    for i in np.arange(number_of_each): 
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
        if(val <= element): 
            


def get_fft(yt_tuple , window_duration , window_start_time): 
    # window works
    tuple_time = yt_tuple[0]
    tuple_val = yt_tuple[1]

    if(window_start_time > tuple_time[-1] - window_duration): 
        window_start_time = tuple_time[-1] - window_duration

    

    

    N = np.array(tuple_time).size
    T = tuple_time[1] - tuple_time[0]
    
    freq = np.linspace(0 , 1/T , N)
    fft = np.fft.fft(tuple_val)

    return (freq[:N//2] , np.abs(fft[:N//2])*(1/N))



# print(np.sin(90))

## start and end of the window

getsine = create_sine(number_of_samples = 50 ,
                        time_frequency = 1 , 
                        time_length = 2 ,
                        init_phase_degree = 0 )
getsine2 = create_sine(number_of_samples = 500,
                        time_frequency = 5 , 
                        time_length = 2, 
                        init_phase_degree=0)

# plt.plot(getsine[0] , getsine[1])
mixed_sine = mix_sines([getsine2 , getsine2] , 2)

plt.figure()
plt.plot(mixed_sine[0] , mixed_sine[1])


fft_pair = get_fft(mixed_sine)
plt.figure()
plt.plot(fft_pair[0] , fft_pair[1])


plt.show()

