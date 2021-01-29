import enum 

"""
    classes containing lists of iterable messages
    can be replaced with a queue of proper type

"""
    
class IterMessageList:
    """ 
        returns iterable lists of messages
    """ 

    def __init__(self , message:list, resettable=False): 
        """
            initializing with a message list 
        """
        if(isinstance(message , str)): 
            ## make a list out of single str
            message = [message]

        self._list_len = 0 
        self._current_list_index = 0 
        self._resettable = resettable
        self._message = message
        self._resettable = resettable

        if(not isinstance(message , list)): 
            raise ValueError("input message of message carrier should be a list not a {}".format(type(message)))

        self._list_len = len(message)


    def append(self , message_iterable): 
        """
            appends a message list to the current one
            used to join two message lists
        """
        # while(message_iterable.has_next()): 
        #     self._message.append(message_iterable.next())
        #     self._list_len += 1
        for message in message_iterable:
            self._message.append(message)
            self._list_len += 1 

    def __iter__(self): 
        """
            Method in iterable interface 
        """
        return self

    def __next__(self): 
        """
            Method in iterable interface
        """
        return self.next()
    
    def next(self)->str: 
        """
            getting the next element of the list
        """
        if(self._current_list_index < self._list_len): 
            message = self._message[self._current_list_index]
            self._current_list_index = self._current_list_index + 1
            
            ## reset the message in the message list
            if(self._current_list_index == self._list_len): 
                if(self._resettable == True): 
                    self._current_list_index = 0

            return message
        else: 
            raise StopIteration("Non-resettable list reached the end")

    def has_next(self):
        """
            check to see if the iterator has a next element
        """
        if(self._list_len > self._current_list_index): 
            return True
        else: 
            return False 

    def reset(self):
        """
            reset the iterator to its initial state
        """ 
        self._current_list_index = 0 

