import abc
import numpy as np 


class MeaningfulList: 
    
    def __init__(self , **kwargs): 
        
        self.__keywords = kwargs.keys()
        self.__dim_lengths = list(kwargs.values())

        for dim_length in self.__dim_lengths:
            if(not isinstance(dim_length , int)):
                raise InvalidArg
            if(not (dim_length) > 0): 
                raise InvalidArg
                
        # print(type(self.__dim_lengths))
        container_size = 1
        for dim_size in self.__dim_lengths: 
            container_size *= dim_size

        self.__container = [0 for _ in range(container_size)]
        self.__container_size = len(self.__container)

    @staticmethod
    def from_list(input_list:list): 
        """
            return an object from list (convert list to meaningful list) 
        """
        if(not isinstance(input_list , list)): 
            """ 
                !Not working with numpy arrays
            """
            raise InvalidArg

        dims = MeaningfulList.__extract_list_dims(input_list)
        dict_input = {}
        ## prepare dimension dict from list entrys
        for idx , value in enumerate(dims): 
            str_var = "dim{}".format(idx)
            dict_input[str_var] = value
        
        answer = MeaningfulList(**dict_input)
        np_input_list:np.array = np.array(input_list)

        idx = 0
        for cell in np_input_list.flat: 
            answer.set_by_linear_index(cell , idx)
            idx += 1
           

        return answer
            

    @staticmethod
    def __extract_list_dims(input_list): 
        if(not type(input_list) == list): 
            return []
        return [len(input_list)]+(MeaningfulList.__extract_list_dims(input_list[0]))

    def __check_keys_validity(self , keys_list): 
        for key in keys_list: 
            if (not key in self.__keywords): 
                raise InvalidArg

    def __put_user_indices_in_order(self , user_indices_dict={}):
        index_in_dim_order = [0 for _ in range(len(self.__keywords))]
        for idx , key in enumerate(self.__keywords):
            ## index_in_dim_order contains user indices with the same ordering
            ## as list 
            index_in_dim_order[idx] = user_indices_dict[key]
        
        return index_in_dim_order
 
    def __check_index_in_range(self , user_index , dim): 
        for idx , val in enumerate(user_index): 
            if(val >= dim[idx]): 
                raise IndexOutOfRange

    def __calculate_linear_idx(self , user_idx:list , dims:list):
        
        shallow_dims = [ val for _, val in enumerate(dims)]
        shallow_user_idx = [val for _, val in enumerate(user_idx)]

        
        if(len(user_idx) != len(dims)): 
            raise InvalidArg

        
        shallow_dims.append(1)
        shallow_user_idx.insert(0 , 0)
        
        shallow_user_idx.reverse()
        shallow_dims.reverse()

        lower_dim_elements_cnt = 1
        counting_steps = 0 

        for enum_idx , _ in enumerate(shallow_user_idx): 
            lower_dim_elements_cnt *= shallow_dims[enum_idx]
            counting_steps += lower_dim_elements_cnt * shallow_user_idx[enum_idx]

        
        return counting_steps

    

    def get_by_name(self , **kwargs):
        """
            setter and getter method are copies with minor differences
        """

        keys = kwargs.keys()
        self.__check_keys_validity(keys)
        if(not len(keys) == len(self.__keywords)): 
            raise MissingArg

        ## put input indices in order in case user has entered
        ## out of order
        ordered_indices = self.__put_user_indices_in_order(kwargs)
        self.__check_index_in_range(user_index=ordered_indices , 
                                        dim=self.__dim_lengths) 
       
        
        linear_idx = self.__calculate_linear_idx(user_idx=ordered_indices , 
                                        dims=self.__dim_lengths)
        
        return self.__container[linear_idx]
        

    def get_by_index_list(self , index:list): 
        """
            Get list by index list
        """
        if(not isinstance(index , list)): 
            raise InvalidArg

        self.__check_index_in_range(user_index=index , 
                                    dim=self.__dim_lengths)
        
        linear_idx =self.__calculate_linear_idx(user_idx=index , 
                                            dims=self.__dim_lengths)

        return self.__container[linear_idx]
        

    def get_by_linear_index(self , index:int): 
        """
            get list by linear index
        """
        if(not isinstance(index , int)): 
            raise InvalidArg

        if(index >= self.__container_size): 
            raise IndexOutOfRange

        return self.__container[index]
        

    def set_by_name(self , val , **kwargs):
        """
            setter and getter are copies with minor differences
        """ 
        keys = kwargs.keys()
        self.__check_keys_validity(keys)
        if(not len(keys) == len(self.__keywords)): 
            raise MissingArg

        ## put input indices in order in case user has entered
        ## out of order
        ordered_indices = self.__put_user_indices_in_order(kwargs)
        self.__check_index_in_range(user_index=ordered_indices , 
                                        dim=self.__dim_lengths) 
       
        
        linear_idx = self.__calculate_linear_idx(user_idx=ordered_indices , 
                                        dims=self.__dim_lengths)

        self.__container[linear_idx] = val

    def set_by_index_list(self , val , index): 
        """
            Setting values in the array by their index
        """
        if(not isinstance(index , list)): 
            raise InvalidArg

        self.__check_index_in_range(user_index=index , 
                                    dim=self.__dim_lengths)
        linear_idx = self.__calculate_linear_idx(user_idx=index , 
                                        dims=self.__dim_lengths)

        self.__container[linear_idx] = val


    def set_by_linear_index(self , val , index:int ): 
        """
            set list by linear index
        """
        if(not isinstance(index , int)): 
            raise InvalidArg

        if(index >= self.__container_size): 
            raise IndexOutOfRange

        self.__container[index] = val
        

    def get_axis(self , axis , other_dims): 
        """
            retuns 1d axis of the list: 
            if axis = 0 and list has a dimension of 3x4 , the function returns a 
            list of 3 elements. In this case other_dims would be [n] n=0..3 
        """
        if(axis >= len(self.get_dimensions())): 
            raise AxisNotFound

        other_dims_cp = [val for val in other_dims]
        other_dims_cp.insert(axis , 0)
        self.__check_index_in_range(user_index = other_dims_cp ,
                                    dim=self.get_dimensions())

        answer = []
        answer_cnt = self.get_dimensions()[axis]
        for idx in range(answer_cnt): 
            current_index:list = [val for val in other_dims]
            current_index.insert(axis , idx)
            
            current_ans = self.get_by_index_list(current_index)
            answer.append(current_ans)

        return answer

    def get_keywords(self): 
        return self.__keywords

    def get_dimensions(self): 
        return self.__dim_lengths

    def dim_count(self): 
        return len(self.get_dimensions)
    
    def items_count(self): 
        return self.__container_size



class InvalidArg(Exception):
    """
        argument not in the list 
    """ 
    pass 

class MissingArg(Exception): 
    """
        not sufficient arguments for indexing 
    """
    pass

class AxisNotFound(Exception): 
    pass

class IndexOutOfRange(Exception): 
    pass

class MismatchingLengths(Exception): 
    pass



# mylist = [[1,2,3] , [4,5,6]]
# bb = MeaningfulList.from_list(mylist)
# items_cnt = bb.items_count()
# # for i in range(2):
# #     print()
# #     for j in range(3): 
# #         print(bb.get_by_index_list([i , j]))

# # print(bb.get_dimensions())
# print(bb.get_axis(axis = 1 , other_dims=[1]))
    