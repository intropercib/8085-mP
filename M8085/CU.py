from . import _utils
from ._data import Data
from ._arithmetic import Arithmetic
from ._logical import Logical
from ._peripheral import Peripheral
from ._stack import Stack

class Control_Unit:

    def __init__(self):
        self.exe_mode = 1 # 1 -> interpret, 0 -> compile 
        self.__token:dict = _utils.get_token()
        self.__data_inst = Data(self.__token)
        self.__arithmetic_inst = Arithmetic(self.__token)
        self.__logical_inst = Logical(self.__token)
        self.__peripheral_inst = Peripheral(self.__token)
        self.__stack_inst = Stack(self.__token)

        self.__inst_set = (
            self.__data_inst.get_inst(),
            self.__arithmetic_inst.get_inst(),
            self.__logical_inst.get_inst(),
            self.__peripheral_inst.get_inst(),
            self.__stack_inst.get_inst()
        )
    
    def inst_list(self):
        return [j for i in self.__inst_set for j in i]
    
    def exe(self,inst:str,prompt:str=None):
            if self.exe_mode:
                for dict in self.__inst_set:
                    for key in dict:
                        if inst == key:
                            if prompt == None:
                                dict[key]()
                            else:        
                                dict[key](prompt)

            elif not self.exe_mode:
                pass

    def show_memory(self):
            return self.__token['memory']        

    def show_register(self):
        return self.__token['register']

    def show_flag(self):
        return self.__token['flag']

    def show_port(self):
        return self.__token['port']

    def get_token(self):
        return self.__token