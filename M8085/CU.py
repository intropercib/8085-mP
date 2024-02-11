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

        self.__inst_set = {
            "Data":self.__data_inst.get_inst(),
            "Arithematic":self.__arithmetic_inst.get_inst(),
            "Logical":self.__logical_inst.get_inst(),
            "Peripheral":self.__peripheral_inst.get_inst(),
            "Stack":self.__stack_inst.get_inst()
        }
    
    def inst_list(self):
        return [j for i in self.__inst_set
                    for j in self.__inst_set[i]
            ]
    
    def exe(self,instType:int,inst:str,prompt:str=None):

        if instType in range(0,5):
            type:str = [_ for _ in self.__inst_set][instType]
        
            if self.exe_mode:
                self.__inst_set[type][inst](prompt)
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