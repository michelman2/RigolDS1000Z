import enum 
from debug import debug_instr as dbg
import numpy as np
import abc
from TransactionMeans import QueueUtil as qutil

class RIGOL_WAVEFORM_FORMAT(enum.Enum): 
    WORD = 0 
    BYTE = 1
    ASCII = 2

    def get_string(self): 
        return str(self.name)

class RIGOL_WAVEFORM_MODE(enum.Enum): 
    NORMAL = 0 
    MAXIMUM = 1
    RAW = 2

    def get_string(self): 
        return str(self.name)

class RIGOL_WAVEFORM_SOURCE(enum.Enum): 
    D0 = 0 
    D1 = 1
    D2 = 2
    D3 = 3
    D4 = 4
    D5 = 5
    D6 = 6
    D7 = 7
    D8 = 8 
    D9 = 9 
    D10 = 10 
    D11 = 11
    D12 = 12
    D13 = 13
    D14 = 14
    D15 = 15
    CHANNEL1 = 16
    CHANNEL2 = 17
    CHANNEL3 = 18
    CHANNEL4 = 19
    MATH = 20

    def get_string(self):
        return str(self.name)


class RIGOL_TRIGGER_HOLDOFF_LIMITS(enum.Enum): 
    MIN = 0 
    MAX = 1 
    def get_value(self): 
        if(self.value == 0):
            # return minimum value in seconds  
            return 0.000000016
        elif(self.value == 1): 
            # return maximum value in seconds
            return 10

class RIGOL_TRIGGER_SWEEP(enum.Enum): 
    AUTO = 1 
    NORMAL = 2
    SINGLE = 3

    def get_string(self): 
        return str(self.name)

class RIGOL_TRIGGER_STATUS(enum.Enum): 
    TD = 1
    WAIT = 2
    RUN = 3 
    AUTO = 4
    STOP = 5

## Rigol trigger coupling
class RIGOL_TRIGGER_COUPLING(enum.Enum): 
    AC = 1 
    DC = 2
    LFreject = 3
    HFreject = 4

    def get_string(self): 
        return str(self.name)

## Rigol trigger mode 
class RIGOL_TRIGGER_MODES(enum.Enum): 
    EDGE = 1
    PULSe = 2
    RUNT = 3
    WIND = 4
    NEDG = 5
    SLOPe = 6
    VIDeo = 7
    PATTern = 8
    DELay = 9 
    TIMeout = 10
    DURation = 11
    SHOLd = 12
    RS232 = 13
    IIC = 14
    SPI = 15

    def get_string(self): 
        return str(self.name)

## RIGOL PROBLE ATTENUATION list 
class RIGOL_PROBE_ATTENUATION_VALUES(enum.Enum): 
    START = -1
    _0_01 = 0 
    _0_02 = 1
    _0_05 = 2 
    _0_1 = 3
    _0_2 = 4
    _0_5 = 5
    _1 = 6
    _2 = 7
    _5 = 8
    _10 = 9
    _20 = 10
    _50 = 11
    _100 = 12
    _200 = 13
    _500 = 14
    _1000 = 15
    END = 16

    def get_string(self):
        var_name = str(self.name)
        var_name_numberify = var_name.replace('_' , '.')[1:]
        return var_name_numberify

    def next(self): 
        v = self.value + 1
        if(v >= RIGOL_PROBE_ATTENUATION_VALUES.END.value):
            return RIGOL_PROBE_ATTENUATION_VALUES.END

        else: 
            return RIGOL_PROBE_ATTENUATION_VALUES(v)

    def prev(self): 
        v = self.value - 1
        if(v <= RIGOL_PROBE_ATTENUATION_VALUES.START.value):
            return RIGOL_PROBE_ATTENUATION_VALUES.START

        else: 
            return RIGOL_PROBE_ATTENUATION_VALUES(v)


## RIGOL CHANNEL IMPEDANCE
class RIGOL_CHANNEL_IMPEDANCE(enum.Enum): 
    IMP_1_MOHM = 0 
    IMP_50_OHM = 1  

    def get_string(self): 
        if(self.value == 0): 
            return "omeg" 
        else: 
            return "fifty"

class RIGOL_CHANNEL_COUPLING(enum.Enum): 
    AC = 0 
    DC = 1 
    GND = 2

    def get_string(self): 
        if(self.value == 0): 
            return "ac"
        elif(self.value == 1): 
            return "dc"
        elif(self.value == 2): 
            return "gnd"
                   


class RIGOL_CHANNEL_IDX(enum.Enum): 
    CH1 = 1 
    CH2 = 2 
    CH3 = 3 
    CH4 = 4

    def get_string(self): 
        return "channel{}".format(self.value)

    def get_data_val(self): 
        return self.value - 1

# check values for the model of rigol 
class RIGOL_BW_OPTIONS(enum.Enum): 
    BW_20Mhz = 0 
    BW_100Mhz = 1
    BW_OFF = 2

# check values for the model of rigol
class RIGOL_MEM_DEPTH_INTERWEAVE(enum.Enum):
    AUTO = 0
    N_14E3 = 1
    N_14E4 = 2
    N_14E5 = 3
    N_14E6 = 4
    N_56E6 = 5


# check values for the model of rigol
class RIGOL_MEM_DEPTH_NON_INTERWEAVE(enum.Enum): 
    AUTO = 0 
    N_7E3 = 1
    N_7E4 = 2
    N_7E5 = 3
    N_7E6 = 4
    N_28E6 = 5


# check values for the model of rigol 
class RIGOL_ACQUIRE_TYPES(enum.Enum): 
    NORMAL = 0
    AVERAGES = 1
    PEAK = 2
    HRE_SOLUTION = 3

class RIGOL_ON_OFF(enum.Enum): 
    OFF = 0
    ON = 1

    def get_string(self): 
        return str(self.name)

class SCPI_RESPONSE_TYPE(enum.Enum): 
    DATA_PAIR = 0 
    PREAMBLE = 1
    CHANNEL_NUMBER = 2

class EXC_IMPROPER_PARAMETER(Exception): 
    pass

class EXC_METHOD_NOT_IMPLEMENTED(Exception): 
    pass

class IcmdParsedObj(abc.ABC): 
    def __init__(self): 
        pass

    
        
    @abc.abstractmethod
    def get_channel(self)->RIGOL_CHANNEL_IDX: 
        pass 

    @abc.abstractmethod
    def get_response_type(self)->SCPI_RESPONSE_TYPE: 
        pass 

    @abc.abstractmethod
    def get_data_x(self):
        pass 

    @abc.abstractmethod
    def get_data_y(self): 
        pass 

    


class cmdObj(qutil.IQueueSiftableObject): 
   
    def __init__(self , cmd_string, needs_answer): 
        self.__answer = ""
        self.__parser = None
        self.__active_channel_for_cmd = None 
        self.__cmd = cmd_string
        self.__needs_answer = needs_answer
       
        ## The cmdObjs can be stacked together 
        ## with the core object's previous_cmd_obj_being None 
        self.__previous_cmd_obj = None

    def needs_answer(self): 
        return self.__needs_answer

    def get_cmd(self): 
        return self.__cmd

    def set_answer(self , answer:str):
        parser:cmdParsedObj = self.get_parser()
        if(parser == None): 
            self.__parser = cmdParsedObj(self.__answer)
        else:
            self.__answer = answer
            parser.set_parser_answer(answer)
            
    def get_answer(self): 
        return self.__answer
        
    def get_parser(self): 
        if(self.__parser == None):            
            self.__parser = cmdParsedObj()
                    
        return self.__parser

    def set_active_channel(self , active_channel): 
        self.__active_channel_for_cmd = active_channel
    
    def get_active_channel(self)->RIGOL_CHANNEL_IDX: 
        return self.__active_channel_for_cmd

    def get_previous_cmd_step(self): 
        return self.__previous_cmd_obj

    def clone_to_cmdParseClone(self , new_x , new_y , added_info={}): 
        """
            clones the object with custom x and y  
        """

        cloned_obj = cmdObj(self.__cmd , self.__needs_answer)
        current_parser = self.get_parser()

        ## parser of the new object holds processed information
        ## the reference to the previous cmd_obj holds one step before processing
        cloned_obj.__parser:IcmdParsedObj = cmdParseCloneObj(
                                            x=new_x ,
                                            y=new_y,
                                            channel=current_parser.get_channel(),
                                            response_type=current_parser.get_response_type(),
                                            additional_info=added_info)
        
    
        cloned_obj.__previous_cmd_obj = self

        return cloned_obj

    def get_sifting_parameter(self):
        if(self.__parser == None): 
            raise qutil.SiftingCharNotFound

        return self.__parser.get_channel()

class cmdParseCloneObj(IcmdParsedObj): 
    
    def __init__(self , x , y , channel , response_type, additional_info={}):
        self.__x = x 
        self.__y = y 
        self.__channel = channel
        self.__response_type = response_type
        self.__additional_info = additional_info
        
    
    def get_channel(self)->RIGOL_CHANNEL_IDX: 
        return self.__channel


    def get_response_type(self)->SCPI_RESPONSE_TYPE: 
        return self.__response_type


    def get_data_x(self):
        return self.__x  


    def get_data_y(self): 
        return self.__y


    def get_additional_info(self)->dict:
        """ 
            Returns additional keyworded info 
        """ 
        return self.__additional_info



class cmdParsedObj(IcmdParsedObj): 
    """
        Class holding parse inforamation of a response received 
        from oscilloscope 
    """

    __response_type = None 
    __x_scale_factor = 1 
    __y_scale_factor = 1 
    __y_origin = 0
    __x_origin = 0 

    def __init__(self , received_resp=None):
        self.channel = None 
        if(received_resp != None): 
            self.__received_resp = received_resp
            self.__parse()
    

    def set_parser_answer(self , received_resp:str): 
        
        self.__received_resp = received_resp
        self.__parse()
        
    def __parse(self):
        """
            tries to parse the string of reponse according to 
            the response type
        """
        
        ## searches for data information in received responses
        if(self.__check_data_answer() != None):    
            response = self.__check_data_answer()
            self.data_idx = response[0]
            self.data_val = response[1]
            self.__response_type = SCPI_RESPONSE_TYPE.DATA_PAIR            
        
        ## searches for preamble information in a response
        elif(self.__check_preamble_answer() != None):
            self.preamble = self.__check_preamble_answer()
            self.__response_type = SCPI_RESPONSE_TYPE.PREAMBLE

        ## searches for channel number in a response
        elif(self.__check_channel_answer() != None): 
            self.channel = RIGOL_CHANNEL_IDX(self.__check_channel_answer())
            self.__response_type = SCPI_RESPONSE_TYPE.CHANNEL_NUMBER

    def get_channel(self)->RIGOL_CHANNEL_IDX: 
        """
            get parsed information about channel index 
        """
        return self.channel

    def get_response_type(self)->SCPI_RESPONSE_TYPE: 
        """
            get response type from parsed information 
        """
        return self.__response_type

    def set_response_type(self, resp:SCPI_RESPONSE_TYPE):
        """
            ???
        """
        if(dbg.flags.LOOPBACK): 
            self.__response_type = resp
    

    def __check_data_answer(self):
        """
            extracting data from response to waveform:data
            so the headerfile looks like this: 
            Nxxxxxxx where x repeats N times
        """
        answer = None 
       
        self._data_header_sharp_sign = self.__received_resp[0]        
        if(chr(self._data_header_sharp_sign) == '#'):             
            self._data_header_N = self.__received_resp[1]
            number = self._data_header_N - 48
            self._data_pts_count = list(self.__received_resp[2 : number + 2])
            self._data_pts_count.reverse()
            tens = 1
            data_pts_count_all = 0
            for digit in self._data_pts_count:                 
                real_digit = digit - 48
                data_pts_count_all = data_pts_count_all + tens * real_digit
                tens = 10 * tens

            data_start_idx = number + 2 
            useful_data = self.__received_resp[data_start_idx : data_start_idx + data_pts_count_all - 1]
            data_value = []
            data_idx = []
            for i, data in enumerate(useful_data): 
                data_value.append(data)
                data_idx.append(i)
            answer = (data_idx , data_value)

        return answer

    def __check_preamble_answer(self): 
        """ 
            checks to see if the variable __received_resp has the 
            format of preamble
        """
        answer = None
        
        try:
            ## decoding data from binary to string format
            temp_received_resp = self.__received_resp.decode()

            ## removing the last element of data, as it is \n char
            temp_received_resp = temp_received_resp[0:len(temp_received_resp)-1]

            ## split data to array 
            split_data = temp_received_resp.split(',')
            
            ## check the number of preamble, specified in the data sheet
            if(len(split_data) == 10): 
                float_preamble = [float(x) for x in split_data]
                answer = float_preamble

        except:
            answer = None 

        return answer

    def __check_channel_answer(self): 
        """ 
            Looks for name "chan" in the response to see if a channel number
            has been set for the oscilloscope
        """
        
        chan_number = None 
        try: 
            lower_resp = self.__received_resp.decode()
            lower_resp = lower_resp.lower()
            
            
            if(lower_resp[0:4] == "chan"): 
                chan_number = int(lower_resp[-2])


        except: 
            pass 
        return chan_number

    def get_data_x_idx(self): 
        return self.data_idx

    def get_data_x(self):
        """
            returns the x value of parsed data from response (if the response
            is data pair)
        """ 
        return list(np.add(np.multiply(self.data_idx , self.__x_scale_factor) , self.__x_origin))

    def get_data_y(self): 
        """
            returns the y value of parsed data from response (if the response 
            is data pair)
        """
        return list(np.subtract(np.multiply(self.data_val , self.__y_scale_factor) , self.__y_offset*self.__y_scale_factor))

    def get_data_y_idx(self): 
        """
            returns the index of y values 
        """
        return self.data_val
    
    def get_preamble(self): 
        """
            returns parsed preamble (if response was preamble) 
        """
        return self.preamble

    def set_x_scale_factor(self , s_factor:float): 
        """
            setting the scale factor of x axis
            (applicable for preamble response) 
        """
        self.__x_scale_factor = s_factor

    def set_y_scale_factor(self , s_factor:float): 
        """
            setting the scale factor of y axis
            (applicable for preamble responses)
        """
        self.__y_scale_factor = s_factor

    def get_y_scale_factor(self)->float: 
        """
            returns scale factor of y axis 
        """
        return self.__y_scale_factor

    def set_y_offset(self , y_offset:float):
        """
            returns scale factor of x axis 
        """ 
        self.__y_offset = y_offset

    def set_x_origin(self , x_orig:float): 
        """
            returns current time offset 
            (applicable for preamble responses) 
        """
        self.__x_origin = x_orig

   
    
class RigolSCPI: 
    def autoscale(self): 
        ## this command does not work when a auto mode is 
        return cmdObj(":autoscale\n" , needs_answer = False)

    def clear(self): 
        ## clears all the waveforms on the screen
        return cmdObj(":clear\n" , needs_answer = False)

    def run(self): 
        ## The same as RUN button on the oscilloscope
        return cmdObj(":run\n" , needs_answer = False)

    def stop(self): 
        ## The same as STOP button on the oscilloscope
        return cmdObj(":stop\n" , needs_answer = False)

    def single(self): 
        ## single trigger on oscilloscope
        return cmdObj(":single\n" , needs_answer = False)

    def tforce(self): 
        ## make a trigger signal forcefully
        return cmdObj(":tforce\n" , needs_answer = False)

    def tlhalf(self): 
        ## sets the trigger to the mid point of trigger
        ## signal amplitude
        return cmdObj(":tlhalf\n" , needs_answer = False)

    def clear_status(self): 
        ## clear all event registers and error queue
        return cmdObj("*cls\n" , needs_answer = False)

    def ese(self): 
        ## Set or query the enable register 
        ## for the standard event status register set.
        return cmdObj("*ese\n" , needs_answer = False)

    
    def identify_device(self): 
        ## Query the device information
        return cmdObj("*idn?\n" , needs_answer = True)

    def is_operation_complete(self): 
        ## query if the operation on the oscilloscope is finished
        return cmdObj("*opc?\n" , needs_answer = True)

    def factory_reset(self): 
        ## resets the device to factory settings
        return cmdObj("*rst\n" , needs_answer = False) 

    def set_sre(self , mask): 
        ## sets the enable register for the state byte register set
        # @param mask: 0 to 255, 0 is the defualt
        command = "*sre {0:.d}\n".format(mask)
        return cmdObj(command , needs_answer = False)

    def query_sre(self): 
        ## queries the enable register for the state byte register set
        return cmdObj("*sre?\n" , needs_answer = True)
    
    def query_stb(self): 
        ## query the condition register for the state byte register set
        return cmdObj("*stb?\n" , needs_answer = True)

    def test(self): 
        ## perform a self test on the device 
        return cmdObj("*tst\n" , needs_answer = True)

    ############################### 
    ## ACQUIRE COMMANDS
    def query_acquire_averages(self): 
        ## query the number of averages in average acquisition mode
        return cmdObj(":acquire:averages?\n" , needs_answer = True)

    def set_acquire_averages(self , number_of_averages): 
        ## sets the number of averages in average acquisition mode
        # number of averages should be 2^n : n = 1 to 13 
        cmd = ":acquire:averages {0:.d}\n".format(number_of_averages)
        return cmdObj(cmd , needs_answer = False)


    def query_acquire_mdepth(self): 
        ## query the number of points that can be stored in the memory for a single trigger
        # in other words, memory depth
        cmd = ":acquire:mdepth?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_acquire_mdepth(self , memory_depth): 
        ## sets the memory depth
        # the memory_depth is from RIGOL_MEM_DEPTH_INTERWEAVE enum or 
        # RIGOL_MEM_DEPTH_NON_INTERWEAVE enum
        cmd = ":acquire:mdepth {0:.d}\n".format(memory_depth)
        return cmdObj(cmd , needs_answer = False)


    def query_sampling_rate(self): 
        ## Query the sampling rate of the device
        cmd  = ":acquire:srate?\n"
        return cmdObj(cmd , needs_answer = True)

    def set_acquire_type(self , acquire_type): 
        ## set the acquire type 
        # the acquire_type should be of type RIGOL_ACQUIRE_TYPES
        if(acquire_type == RIGOL_ACQUIRE_TYPES.NORMAL): 
            parameter = "normal\n"
        elif(acquire_type == RIGOL_ACQUIRE_TYPES.AVERAGES):
            parameter = "averages\n"
        elif(acquire_type == RIGOL_ACQUIRE_TYPES.PEAK): 
            parameter = "peak\n"
        elif(acquire_type == RIGOL_ACQUIRE_TYPES.HRE_SOLUTION): 
            parameter = "hresolution\n"
        else: 
            raise EXC_IMPROPER_PARAMETER

        cmd = ":acquire:type {}\n".format(parameter)
        return cmdObj(cmd , needs_answer = False)


    def query_acquire_type(self): 
        cmd = ":acquire:type?\n"
        return cmdObj(cmd , needs_answer = True)
    
    def query_antialias_function_status(self): 
        ## Query antialias function status
        cmd = ":acquire:aalias?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_antialias_function(self , on_off): 
        ## turn antialias function on or off
        if(on_off == RIGOL_ON_OFF.ON): 
            parameter = "on" 
        elif(on_off == RIGOL_ON_OFF.OFF): 
            parameter = "off"
        else: 
            raise EXC_IMPROPER_PARAMETER

        cmd = ":acquire:aalias {}\n".format(parameter)
        return cmdObj(cmd , needs_answer = False)

############################### channel commands 
    def set_channel_bw_limit(self , channel , bw_limit): 
        ## set channel bandwidth limit
        # the channel has to be chosen from RIGOL_CHANNEL_IDX
        if(bw_limit == RIGOL_BW_OPTIONS.BW_100Mhz): 
            bw = "100M" 
        elif(bw_limit == RIGOL_BW_OPTIONS.BW_20Mhz): 
            bw = "20M" 
        elif(bw_limit == RIGOL_BW_OPTIONS.BW_OFF): 
            bw = "OFF"
        
        ch = self.__check_channel_number(channel)

        cmd = ":channel{0}:bwlimit {1}\n".format(ch , bw)
        return cmdObj(cmd , needs_answer = False)


    def query_channel_bw_limit(self , channel): 
        ## query the bandwidth limits of a channel
        # the channel has to be chosen from RIGOL_CHANNEL_IDX
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:bwlimit?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)
    
    def set_channel_coupling(self , channel , coupling):
        ## set channel coupling from one of options in RIGOL_CHANNEL_COUPLING
        ch = self.__check_channel_number(channel)
        
        if(coupling ==  RIGOL_CHANNEL_COUPLING.AC): 
            couple_str = "ac" 
        elif(coupling == RIGOL_CHANNEL_COUPLING.DC): 
            couple_str = "dc" 
        elif(coupling == RIGOL_CHANNEL_COUPLING.GND): 
            couple_str = "gnd"
        else: 
            raise EXC_IMPROPER_PARAMETER

        cmd = ":channel{0}:coupling {1}\n".format(ch , couple_str)
        return cmdObj(cmd , needs_answer = False)

    def query_channel_coupling(self , channel): 
        ## query channel coupling 
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:coupling?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)

    def set_channel_display(self , channel , on_off): 
        ## display or hide a channel
        ch = self.__check_channel_number(channel)
        if(on_off == RIGOL_ON_OFF.ON): 
            on_off_str = "on"
        elif(on_off == RIGOL_ON_OFF.OFF): 
            on_off_str = "off"

        cmd = ":channel{0}:display {1}\n".format(ch , on_off_str)
        return cmdObj(cmd , needs_answer = False)

    def query_channel_display(self , channel): 
        ## query the status of a channel on display (on or off)
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:display?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)

    def set_channel_invert(self , channel , invert_on_off): 
        ## inverts a channel if invert parameter is on 
        ch = self.__check_channel_number(channel)
        on_off = self.__check_channel_on_off(invert_on_off)
        cmd = ":channel{0}:invert {1}\n".format(ch , on_off)
        return cmdObj(cmd , needs_answer = False)


    def query_channel_invert(self, channel): 
        ## query channel inversion status
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:invert?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)


    def set_channel_offset(self , channel , offset): 
        ## set channel offset, must check offset values        
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:offset {1}\n".format(ch , offset)
        return cmdObj(cmd , needs_answer = False)


    def query_channel_offset(self , channel): 
        ## query channel offset
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:offset?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)


    def set_channel_scale(self , channel , scale): 
        ## set channel vertical scale 
        # @param scale: 
        #        When input impedance is 50 ohm and probe ratio is 1x: 500 uV/div to 1 V/div
        #        When input impedance is 1 Mohm and probe ratio is 1x: 500 uV/div to 10 V/div
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:scale {1}\n".format(ch , scale)
        return cmdObj(cmd , needs_answer = False)


    def query_channel_scale(self , channel): 
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:scale?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)


    def set_probe_attenuation(self , channel , attenuation): 
        ## Set the probe attenuation
        #  the method get_string returns the proper format of attenuation 
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:probe {1}\n".format(ch , attenuation.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_probe_attenuation(self , channel): 
        ch = self.__check_channel_number(channel)
        cmd = ":channel{0}:probe?\n".format(ch)
        return cmdObj(cmd , needs_answer = True)

    ########################## Trigger commands


    def set_trigger_mode(self , trigger_mode): 
        ## set the trigger mode of the oscilloscope
        # @param: trigger_mode should be chosen from RIGOL_TRIGGER_MODES Enum
        cmd = ":trigger:mode {0}\n".format(trigger_mode.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_trigger_mode(self): 
        ## query the trigger mode of oscilloscope
        cmd = ":trigger:mode?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_trigger_coupling(self , trigger_coupling): 
        ## Set the trigger coupling of oscilloscope
        # @param: trigger_coupling should be from RIGOL_TRGGER_COUPLING
        cmd = ":trigger:coupling {0}\n".format(trigger_coupling.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_trigger_coupling(self): 
        ## Query the trigger coupling
        cmd = ":trigger:coupling?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_trigger_status(self): 
        ## Query the trigger status of the device
        cmd = ":trigger:status?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_trigger_sweep(self , trigger_sweep): 
        ## Set the trigger sweep mode 
        # @param trigger_sweep selects the trigger sweep mode 
        cmd = ":trigger:sweep {0}\n".format(trigger_sweep.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_trigger_sweep(self): 
        ## Query the trigger sweep 
        cmd = ":trigger:sweep?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_trigger_holdoff(self , value): 
        ## Set trigger hold off value 
        # @param value: hold off time in seconds, should be withing minimum and maximum limits of 
        #               RIGOL_TRIGGER_HOLDOFF_LIMITS
        if(value > RIGOL_TRIGGER_HOLDOFF_LIMITS.MAX.get_value()): 
            raise EXC_IMPROPER_PARAMETER
        if(value < RIGOL_TRIGGER_HOLDOFF_LIMITS.MIN.get_value()): 
            raise EXC_IMPROPER_PARAMETER
        
        cmd = ":trigger:holdoff {0}\n".format(value)
        return cmdObj(cmd , needs_answer = False)


    def query_trigger_holdoff(self): 
        ## Query the trigger hold off
        cmd = ":trigger:holdoff?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_trigger_noise_reject(self , on_off): 
        ## Set the trigger noise reject on or off
        # @param on_off: param selected from ON_OFF ENUM
        cmd = ":trigger:nreject {0}\n".format(on_off.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_trigger_noise_reject(self): 
        ## Query the status of noise reject in trigger 
        cmd = ":trigger:nreject?\n"
        return cmdObj(cmd , needs_answer = True)

    def query_trigger_position(self): 
        ## Query the position of trigger in the internal memory
        cmd = ":trigger:position?\n"
        return cmdObj(cmd , needs_answer = True)
    #####################################################
    #                                                   #
    #   Some trigger methods are not yet developed      #
    #                                                   #
    #                                                   #
    #####################################################

    def set_waveform_source(self , wave_source):
        ## Set the source of waveform from which data needs to be read
        # @param wave_source: should be from RIGOL_WAVEFORM_SOURCE
        cmd = ":waveform:source {0}\n".format(wave_source.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_waveform_source(self): 
        ## Query the source of wave from which data needs to be read 
        cmd = ":waveform:source?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_waveform_mode(self , wave_mode): 
        ## Set the mode of waveform which needs to be read
        # @param wave_mode: should be from RIGOL_WAVEFORM_MODE
        cmd = ":waveform:mode {0}\n".format(wave_mode.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_waveform_mode(self): 
        ## Query the mode of waveform
        cmd = ":waveform:mode?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_waveform_format(self , data_format): 
        ## Set the format of data retrieved from the device
        # @param data_format : should be selected from RIGOL_DATA_FORMAT
        cmd = ":waveform:format {0}\n".format(data_format.get_string())
        return cmdObj(cmd , needs_answer = False)


    def query_waveform_format(self): 
        ## Query the format of data retrieved from the device
        cmd = ":waveform:format?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_data(self): 
        ## Query data samples from oscilloscope 
        #   proper options should be set before calling this function 
        cmd = ":waveform:data?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_x_increment(self): 
        ## Query the time difference between two sampled data points
        #  related to the normal mode
        #  NORMAL mode: x_increment = timescale / 100 
        #  RAW mode : x_increment = 1 / sample rate 
        #  MAX mode : if the instrument is running x_increment = timescale / 100
        #             if the instrument is stopped x_increment = 1 / samplerate
        cmd = ":waveform:xincrement?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_data_x_origin(self): 
        ## Query the start of the waveform data
        #  NORMAL mode: returns the start time shown on the screen 
        #  RAW mode: returns the start time of the waveform in the memory 
        #  MAX mode: if the instrument is running x_origin = ? 
        cmd = ":waveform:xorigin?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_x_reference(self): 
        ## Query the reference time of the specified channel source in x direction
        cmd = ":waveform:xreference?\n"
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_y_increment(self): 
        ## Query the y increment of the specified channel source
        #   NORMAL mode : y_increment = verticalScale / 25 
        #   RAW mode:     y_increment = related to the verticalscale of the internal waveform
        #   MAX mode:     instrument is running: y_increment = verticalScale / 25
        #                 instrument is stopped: y_increment = related to hte verticalScale of the internal waveform
        cmd = ":waveform:yincrement?\n"
        return cmdObj(cmd , needs_answer = True)
    

    def query_waveform_y_origin(self):
        ## Query the y origin of the waveform
        #   NORMAL mode : y_origin = VerticalOffset/Yincrement
        #   RAW    mode : y_origin = yorigin is related to the VerticalScale of the internal waveform and th e
        #                            VerticalScale currently selected
        cmd = ":waveform:yorigin?\n"
        return cmdObj(cmd , needs_answer = True)

    def query_waveform_y_reference(self): 
        ## Query the y reference of the waveform
        #   NORMAL mode ....
        cmd = ":waveform:yreference?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_waveform_start_point(self , start_point):
        ## Set start point of reading data points
        #   set waveform start point
        cmd = ":waveform:start {0}\n".format(start_point)
        return cmdObj(cmd , needs_answer = False)


    def query_waveform_start_point(self): 
        ## Query the start point of the waveform
        cmd = ":waveform:start?\n"
        return cmdObj(cmd , needs_answer = True)


    def set_waveform_stop_point(self , stop_point): 
        ## Set stop point of waveform data
        # 
        cmd = ":waveform:stop {0}\n".format(stop_point)
        return cmdObj(cmd , needs_answer = True)


    def query_waveform_stop_point(self): 
        cmd = ":waveform:stop?\n"
        return cmdObj(cmd , needs_answer = True)

    def query_waveform_preamble(self): 
        ## Query the waveform preamble: 
        #  The result of this request is as follows: 
        #  1)format 2)type 3)points 4)count 5)xincrement
        #  6)xorigin 7)xreference 8)yincrement
        #  9)yorigin 10)yreference
        cmd = ":waveform:preamble?\n"
        return cmdObj(cmd , needs_answer = True)

    def __check_channel_number(self , channel_index): 
        if(channel_index == RIGOL_CHANNEL_IDX.CH1): 
            param = "1" 
        elif(channel_index == RIGOL_CHANNEL_IDX.CH2): 
            param = "2" 
        elif(channel_index == RIGOL_CHANNEL_IDX.CH3): 
            param = "3" 
        elif(channel_index == RIGOL_CHANNEL_IDX.CH4): 
            param = "4"
        else: 
            raise EXC_IMPROPER_PARAMETER
        return param


    def __check_channel_on_off(self , channel_on_off): 
        if(channel_on_off  == RIGOL_ON_OFF.ON): 
            param = "on" 
        elif(channel_on_off == RIGOL_ON_OFF.OFF): 
            param = "off" 
        else: 
            raise EXC_IMPROPER_PARAMETER

        return param 

    def __check_impedance(self , channel_impedance): 
        if(channel_impedance == RIGOL_CHANNEL_IMPEDANCE.IMP_1_MOHM): 
            param = "omeg"
        elif(channel_impedance == RIGOL_CHANNEL_IMPEDANCE.IMP_50_OHM): 
            param = "fifty"
        else: 
            raise EXC_IMPROPER_PARAMETER

        return param


