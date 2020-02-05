class RigolRespProc: 

    def __init__(self , binary_resp): 
        self.__binary_resp = binary_resp 

    def getHeader(self): 
        ## This class is made when only one command of type WAVEFORM:DATA is considered 
        # so the headerfile looks like this: 
        # #Nxxxxxxx where x repeats N times
        self._data_header_sharp_sign = self.__binary_resp[0]        
        if(chr(self._data_header_sharp_sign) == '#'):             
            self._data_header_N = self.__binary_resp[1]
            number = self._data_header_N - 48
            self._data_pts_count = list(self.__binary_resp[2 : number + 2])
            self._data_pts_count.reverse()
            tens = 1
            data_pts_count_all = 0
            for digit in self._data_pts_count:                 
                real_digit = digit - 48
                data_pts_count_all = data_pts_count_all + tens * real_digit
                tens = 10 * tens

            data_start_idx = number + 2 
            useful_data = self.__binary_resp[data_start_idx : data_start_idx + data_pts_count_all - 1]
            data_value = []
            data_idx = []
            for i, data in enumerate(useful_data): 
                data_value.append(data)
                data_idx.append(i)
            return (data_idx , data_value)