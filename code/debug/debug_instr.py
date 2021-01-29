
class flags: 
    DEBUG = False
    LOOPBACK = False
    PRINT=False

    is_status_logged = False

    @staticmethod
    def cond_print(item): 
        if(False): 
            print(item)

    
    @staticmethod
    def get_flags_logged(cls): 
        if(not cls.is_status_logged): 
            import logging
            main_logger = logging.getLogger("main_logger")
            main_logger.warning("debug_instr.py DEBUG={} , LOOPBACK={} , PRINT={}".format(cls.DEBUG, cls.LOOPBACK , cls.PRINT))
            cls.is_status_logged = True



flags.get_flags_logged(flags)