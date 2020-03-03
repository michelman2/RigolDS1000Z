
import numpy as np

class SineCreator: 

    def __init__(self): 
        pass 

    
    def create_sine(self, number_of_samples, time_frequency ,
                        time_length ,
                        init_phase_degree=0): 

        init_phase_radian = init_phase_degree * np.pi / (180)
        
        x = np.linspace(0 , time_length , number_of_samples)
        y = np.sin(2 * np.pi * time_frequency * x + init_phase_radian)

        return (x , y)

    def mix_sines(self , sine_tuple_arrays , 
                    number_of_each):
    
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
        