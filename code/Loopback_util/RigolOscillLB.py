""" 
    A rigol oscilloscope virtual loopback model
    The data functionality can be made  

"""
import ITCPLoopback
import enum 
from Rigol_Lib import RigolSCPI
from matplotlib import pyplot as plt
import numpy as np

class RigolOscillLB(ITCPLoopback.ITCPloopback): 

    def __init__(self): 
        self.__oscill_model:OscilloscopeStateModel = OscilloscopeStateModel()
        self.__data_generator:DataGenerator = DataGenerator()
        super()
        pass 

    """
        The recv function, implements is invoked when data from 
        TCP socket is expected
    """
    def recv(self , *flags): 
        last_resp_type = self.__oscill_model.get_last_response_type()
        answer = None 

        if (last_resp_type == RigolSCPI.SCPI_RESPONSE_TYPE.PREAMBLE):
            answer = self.__get_bytearray_preamble()
        elif(last_resp_type == RigolSCPI.SCPI_RESPONSE_TYPE.DATA_PAIR): 
            answer = self.__get_bytearray_data()

        return answer
        

    """
        Send and receive functions in the Loopback module 
        are connected to receive and send from an outer module 

        Loopback only works if commands are sent separately
    """
    def send(self, byte_input , *flags): 
        message_string:str = byte_input.decode()
        
        ## message discarded in case it is run
        self.__decode_recv_command(message_string)

        
    def __decode_recv_command(self , message_string:str):
        
        
        ## if the received message is "run", ignore the message
        if("run" in message_string): 
            pass 
        
        elif(":waveform:source" in message_string):
            if("?" in message_string): 
                ## TODO: implement handling data request
                raise NOT_IMPLEMENTED
            
            else: 
                if("ch1" in message_string or "channel1" in message_string): 
                    self.__oscill_model.set_active_channel(RigolSCPI.RIGOL_CHANNEL_IDX.CH1)
                elif("ch2" in message_string or "channel2" in message_string): 
                    self.__oscill_model.set_active_channel(RigolSCPI.RIGOL_CHANNEL_IDX.CH2)
                elif("ch3" in message_string or "channel3" in message_string): 
                    self.__oscill_model.set_active_channel(RigolSCPI.RIGOL_CHANNEL_IDX.CH3)
                elif("ch4" in message_string or "channel4" in message_string): 
                    self.__oscill_model.set_active_channel(RigolSCPI.RIGOL_CHANNEL_IDX.CH4)
        

        elif(":waveform:format" in message_string): 
            if("?" in message_string):
                raise NOT_IMPLEMENTED
            else:  
                ## set a default waveform format
                wave_format = RigolSCPI.RIGOL_WAVEFORM_FORMAT.BYTE

                ## Then parse string message
                if("ascii" in message_string): 
                    wave_format = RigolSCPI.RIGOL_WAVEFORM_FORMAT.ASCII
                elif("byte" in message_string):
                    wave_format = RigolSCPI.RIGOL_WAVEFORM_FORMAT.BYTE
                elif("word" in message_string): 
                    wave_format = RigolSCPI.RIGOL_WAVEFORM_FORMAT.WORD
                
                self.__oscill_model.set_waveform_format(wave_format)
        
            
        elif(":waveform:preamble?" in message_string ): 
            self.__oscill_model.set_last_response_type(RigolSCPI.SCPI_RESPONSE_TYPE.PREAMBLE)

        elif(":waveform:data?" in message_string): 
            self.__oscill_model.set_last_response_type(RigolSCPI.SCPI_RESPONSE_TYPE.DATA_PAIR)


    def __get_bytearray_preamble(self):  
        preamble:list = self.__data_generator.get_preamble()
        preamble_string = str(preamble[0])
        for _ , number in enumerate(preamble[1:]):
            preamble_string += ","
            preamble_string += str(number)
            
        preamble_string += "\n"
        return preamble_string.encode()


    def __get_bytearray_data(self): 
        values:list = self.__data_generator.get_data()
        header_str = "#9{:09d}".format(len(values))
        
        byte_arr_header = bytearray()
        byte_arr_header.extend(map(ord , header_str))

        byte_arr_values = bytearray()
        for _, discretized_val in enumerate(values): 
            discretized_val = int(discretized_val)
            byte_arr_values.append(discretized_val)
        byte_arr_values.append(ord('\n'))

        
        answer = bytes(byte_arr_header + byte_arr_values)

        return answer
        
    
        
    def print_oscill_model(self): 
        print("current active channel : {}".format(self.__oscill_model.get_active_channel()))
        print("current response type : {}".format(self.__oscill_model.get_last_response_type()))
        self.__get_bytearray_preamble()

class OscilloscopeStateModel: 
    
    def __init__(self): 
        ## The last active channel selected by the user
        self.__last_active_channel = RigolSCPI.RIGOL_CHANNEL_IDX.CH1

        ## __last_resp_type = selecting between DATA_PAIR, PREAMBLE
        ## not a real variable in oscilloscope
        self.__last_resp_type = RigolSCPI.SCPI_RESPONSE_TYPE.DATA_PAIR
        
        ## Format of the response returned by the oscilloscope
        self.__last_wave_format = RigolSCPI.RIGOL_WAVEFORM_FORMAT.BYTE

    def set_last_response_type(self , last_reps_type:RigolSCPI.SCPI_RESPONSE_TYPE): 
        self.__last_resp_type = last_reps_type

    def get_last_response_type(self)->RigolSCPI.SCPI_RESPONSE_TYPE: 
        return self.__last_resp_type

    def set_waveform_format(self , wave_format:RigolSCPI.RIGOL_WAVEFORM_FORMAT): 
        self.__last_wave_format = wave_format

    def get_waveform_format(self)->RigolSCPI.RIGOL_WAVEFORM_FORMAT: 
        return self.__last_wave_format

    def set_active_channel(self , channel:RigolSCPI.RIGOL_CHANNEL_IDX): 
        self.__last_active_channel = channel

    def get_active_channel(self)->RigolSCPI.RIGOL_CHANNEL_IDX: 
        return self.__last_active_channel


""" 
    Simulate data sampling of an oscilloscope 
    The preamble holds x_increment , y_increment, references and origins
"""
class DataGenerator: 
    
    def __init__(self): 
        self.x_increment = 1
        self.y_increment = 1
        self.y_origin = 0 
        self.x_origin = 0 
        self.y_reference = 0
        self.x_reference = 0 
        self.points = 1200     

    def get_data(self): 
        
        index = range(self.points)
        y = np.sin(np.multiply(2 * 0.01 * np.pi  , index))        
        digitized = self.__digitize_data(y)
        return digitized

    def set_points_count(self , points_count:int): 
        self.points = points_count

    def set_scales( self , xscale = -1 , yscale = -1):
        if(xscale == -1): 
            xscale = self.x_increment
        if(yscale == -1): 
            yscale = self.y_increment

        self.x_increment = xscale
        self.y_increment = yscale
        # print("in rig lb{}:{}".format(self.x_increment , self.y_increment))

    """
        Simulating the function of an ADC
        adc_resolution = adc resolution

    """
    def __digitize_data(self , data ,  adc_resolution=8 ): 

        out_max = np.power(2 , adc_resolution) - 1 
        
        data_min = np.min(data)
        
        data = np.subtract(data , data_min)
        
        data_max = np.max(data)
        self.set_scales(yscale = data_max / out_max)
        
        data = np.divide(data , self.y_increment)   
        self.y_reference = -1 * np.floor(np.divide(data_min , self.y_increment))  
        digitized = np.floor(data)
        
        ## cut off data more than max data out
        digitized_cut = []
        for _ , data_point in enumerate(digitized): 
            if(data_point > out_max): 
                digitized_cut.append(int(out_max))
            else: 
                digitized_cut.append(int(data_point))

        
        return digitized_cut


    """
        returns the values of preamble that are related to data
        points , count , 
        xincrement , xorigin , xreference , 
        yincrement , yorigin , yreference 
    """
    def get_preamble(self)->list: 
        dformat = 0
        dtype = 0 
        points = self.points
        count = 0 
        
        return [dformat , dtype , points , count , 
                self.x_increment , self.x_origin , self.x_reference ,
                self.y_increment , self.y_origin , self.y_reference]
    
class NOT_IMPLEMENTED(Exception): 
    pass 


# cmd_wav_source = ":waveform:source"

# cmd_req_format = ":waveform:format?"
# cmd_req_preamb = ":waveform:preamble?"
# cmd_req_data = ":waveform:data?"

# loopback = RigolOscillLB()
# cmd_wav_source = cmd_wav_source + " ch2"
# loopback.send(cmd_wav_source.encode())
# loopback.send(cmd_req_preamb.encode())
# print(loopback.recv(100))

# degen = DataGenerator()
# a = degen.get_data()
# plt.show()