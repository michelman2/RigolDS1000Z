import enum 
import abc

## abstract class as an interface for iterating through message lists
#  Any class implementing this has to be iterable
class MessageIterable(abc.ABC): 
    def next(self): 
        pass 
    def has_next(self): 
        pass 

## iterator classes for getting messages
class IterSingleMessage(MessageIterable): 
    def __init__(self , message): 
        self.__message = message

    def next(self): 
        return self.__message
    
class IterMessageList(MessageIterable): 
    __list_len = 0 
    __current_list_index = 0 

    def __init__(self , message): 
        self.__message = message

        if(not isinstance(message , list)): 
            raise EXC_INVALID_ARG

        self.__list_len = len(message)


    def append(self , message_iterable): 
        while(message_iterable.has_next()): 
            self.__message.append(message_iterable.next())
            self.__list_len += 1

    
    def next(self): 
        if(self.__list_len > self.__current_list_index): 
            message = self.__message[self.__current_list_index]
            self.__current_list_index = self.__current_list_index + 1
            return message
        else: 
            raise ITERABLE_ACCESS_OUTOFRANGE

    def has_next(self): 
        if(self.__list_len > self.__current_list_index): 
            return True
        else: 
            return False 

    def reset(self): 
        self.__current_list_index = 0 

    


# class IterMessageStack(MessageIterable):     
    
#     __message  = []

#     def __init__(self, message_list): 
#         self.__message = message_list
#         if(not isinstance(message_list , list)): 
#             raise EXC_INVALID_ARG
        

#     def next(self): 
#         if(len(self.__message) > 0): 
#             current_message = self.__message[0]
#             self.__message.remove(self.__message[0])
#             return current_message
#         else: 
#             raise ITERABLE_ACCESS_OUTOFRANGE 

#     def has_next(self): 
#         if(len(self.__message) > 0 ): 
#             return True
#         else: 
#             return False 

#     def append(self , message_iterable): 
#         while(message_iterable.has_next()): 
#             self.__message.append(message_iterable.next())
            


class EXC_INVALID_ARG(Exception): 
    pass 

class ITERABLE_ACCESS_OUTOFRANGE(Exception): 
    pass
