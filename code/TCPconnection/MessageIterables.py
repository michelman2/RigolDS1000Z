import enum 
import abc


"""
    classes containing lists of iterable messages
    can be replaced with a queue of proper type

"""

## abstract class as an interface for iterating through message lists
#  Any class implementing this has to be iterable
# class MessageIterable(abc.ABC): 
#     def next(self): 
#         pass 
#     def has_next(self): 
#         pass 


    
class IterMessageList:
    """ 
        returns iterable lists of messages
    """ 
    __list_len = 0 
    __current_list_index = 0 

    __resettable = False

    def __init__(self , message:list, resettable=False): 
        """
            initializing with a message list 
        """
        self.__message = message
        self.__resettable = resettable

        if(not isinstance(message , list)): 
            raise EXC_INVALID_ARG

        self.__list_len = len(message)


    def append(self , message_iterable): 
        """
            appends a message list to the current one
            used to join two message lists
        """
        while(message_iterable.has_next()): 
            self.__message.append(message_iterable.next())
            self.__list_len += 1

    
    def next(self)->str: 
        """
            getting the next element of the list
        """
        if(self.__list_len > self.__current_list_index): 
            message = self.__message[self.__current_list_index]
            self.__current_list_index = self.__current_list_index + 1
            
            ## reset the message in the message list
            if(self.__current_list_index == self.__list_len): 
                if(self.__resettable == True): 
                    self.__current_list_index = 0

            return message
        else: 
            raise ITERABLE_ACCESS_OUTOFRANGE

    def has_next(self):
        """
            check to see if the iterator has a next element
        """
        if(self.__list_len > self.__current_list_index): 
            return True
        else: 
            return False 

    def reset(self):
        """
            reset the iterator to its initial state
        """ 
        self.__current_list_index = 0 

    


class EXC_INVALID_ARG(Exception): 
    pass 

class ITERABLE_ACCESS_OUTOFRANGE(Exception): 
    pass
