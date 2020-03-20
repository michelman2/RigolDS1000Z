from TransactionMeans import MeaningfulList
import abc
from Gui import bundlePlotToGui
from MessageIterables import IterMessageList

class BundlingStrategy(abc.ABC): 

    def __init__(self): 
        pass 

    
    @abc.abstractmethod
    def bundle_all_to_canvas(self, canvas_list:MeaningfulList.MeaningfulList , bundler): 
        pass


class RowWiseBundler(BundlingStrategy): 
    
    def bundle_all_to_canvas(self , canvas_list:MeaningfulList.MeaningfulList , 
                                    bundlers_group:list): 
        if(len(canvas_list.get_dimensions()) > 2): 
            raise TooManyDimensionsError

        if((canvas_list.get_dimensions()[0]) != len(bundlers_group)): 
            # print("aaa{}".format(len(bundlers_group)))
            raise DimensionMismatch

        for row_idx in range(len(bundlers_group)): 
            canvas_row = canvas_list.get_axis(axis=1 , other_dims=[row_idx])
            bundlers_group[row_idx].setCanvas(canvas_row)


class BundleById(BundlingStrategy): 
    
    def bundle_all_to_canvas(self , canvas_list:MeaningfulList.MeaningfulList ,
                                bundlers_group:list):
        try:
            for bundler in bundlers_group:  
                canvas = canvas_list.get_by_index_list(bundler.id())
                bundler.setCanvas(canvas)
        except: 
            raise




class BundlersGroup: 

    def __init__(self , bundling_strategy:BundlingStrategy=None):
        self.__bundlers_group = []
        self.__bundling_strategy:BundlingStrategy = None
        self.__bundled_canvas:MeaningfulList.MeaningfulList = None

    def add_bundler(self , bundler:bundlePlotToGui.IbundlePlotToGui): 
        self.__bundlers_group.append(bundler)
        self.__invalidate_iterator()

    def bundle_all_to_canvas(self): 
        if(self.__bundled_canvas == None): 
            raise BundleTargetNoneError

        if(self.__bundling_strategy == None): 
            raise StrategyNotDefined

        
        # for bundler in self.__bundlers_group: 
        self.__bundling_strategy.bundle_all_to_canvas(self.__bundled_canvas , self.__bundlers_group)

    def remove_bundler(self , bundler:bundlePlotToGui.IbundlePlotToGui): 
        try: 
            self.__bundlers_group.remove(bundler)
            self.__invalidate_iterator()
        except: 
            pass 
    

    def set_bundler_strategy(self , strate:BundlingStrategy): 
        self.__bundling_strategy = strate


    def set_canvas(self , bundled_canvases):
        if(isinstance(bundled_canvases , list)): 
            proper_input = MeaningfulList.MeaningfulList.from_list(bundled_canvases)
        else: 
            proper_input = bundled_canvases

        self.__bundled_canvas:MeaningfulList.MeaningfulList = proper_input 

    def update_all(self): 
        for bundler in self.__bundlers_group: 
            ## typing for easier coding
            temp_bundler:bundlePlotToGui.IbundlePlotToGui = bundler
            temp_bundler.startBundling()
            

    def update_next(self): 
        if(self.__bundle_iterator == None): 
            self.__bundle_iterator = IterMessageList(self.__bundlers_group, 
                                                    resettable=True)
        
        if(self.__bundle_iterator.has_next()): 
            current_bundlder:bundlePlotToGui.IbundlePlotToGui = self.__bundle_iterator.next()
            current_bundlder.startBundling()

        else: 
            raise EmptyGroupIteratorError


    def __invalidate_iterator(self): 
        self.__bundle_iterator = None 


class EmptyGroupIteratorError(Exception): 
    pass

class BundleTargetNoneError(Exception): 
    pass

class StrategyNotDefined(Exception): 
    pass

class TooManyDimensionsError(Exception): 
    pass

class DimensionMismatch(Exception): 
    pass