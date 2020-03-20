import abc
from Rigol_Lib import RigolSCPI as rs
import time

class DataExpander(abc.ABC): 
    """
        Makes several data out of one input data based on different rules 
    """
    def __init__(self , history_depth): 
        self.history_depth = history_depth

    @abc.abstractmethod
    def expand_data(self , processed_token): 
        pass 




class cmdObjHistoryExctractor(DataExpander): 
    """
        exctracts the history of a cmdObj command
    """
    def __init__(self , history_depth): 
        super().__init__(history_depth)


    def expand_data(self , token:rs.cmdObj):
        answer_list = []

        if(not isinstance(token , rs.cmdObj)): 
            raise InvalidArgTypeError

        temp_token = token 
        # answer_list.append(temp_token)
        while(temp_token != None): 
            answer_list.append(temp_token)
            temp_token = temp_token.get_previous_cmd_step()
            
        
        if(len(answer_list) - 1 < self.history_depth): 
            raise NotEnoughHistoryError

        return answer_list
            


class InvalidArgTypeError(Exception): 
    pass

class NotEnoughHistoryError(Exception): 
    pass