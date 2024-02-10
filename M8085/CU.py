from . import _utils
from ._data import Data
from ._arithmetic import Arithmetic
from ._logical import Logical
from ._peripheral import Peripheral
#Import

class Control_Unit:

    def __init__(self):
        self.exe_mode = 1 # 1 -> interpret, 0 -> compile 
        self.__token:dict = _utils.get_token()
        self.__data_inst = Data(self.__token)
        self.__arithmetic_inst = Arithmetic(self.__token)
        self.__logical_inst = Logical(self.__token)
        self.__peripheral_inst = Peripheral(self.__token)
        
    def inst_set(self):
        return {
            "Data":self.__data_inst.get_inst(),
            "Arithematic":self.__arithmetic_inst.get_inst(),
            "Logical":self.__logical_inst.get_inst(),
            "Peripheral":self.__peripheral_inst.get_inst()
        }
    
    def show_memory(self,ic=True):
        if ic:
            return self.__token['memory']
        else:
            _utils.load_memory(arg=self.__token)
            return self.__token        

    def show_register(self,ic=True):
        if ic:
            return self.__token['register']
        else:
            _utils.load_memory(arg=self.__token)
            return self.__token        

    def show_flag(self,ic=True):
        if ic:
            return self.__token['flag']
        else:
            _utils.load_memory(arg=self.__token)
            return self.__token        

    def show_port(self,ic=True):
        if ic:
            return self.__token['port']
        else:
            _utils.load_memory(arg=self.__token)
            return self.__token        



    def check_param(self,inst:str,arg:str):
        prompt = arg.upper().replace(' ', '').split(',')

        if self.__param_rule[inst][0] == 0:
            if len(prompt[0]) >= 1: return 'SyntaxError'

        elif self.__param_rule[inst][0] == 1:

            if len(prompt[0]) != self.__param_rule[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in self.__token['register'].keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in self.__token['memory'].keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in self.__token['port'].keys(): return 'DataError'
            else: return prompt

        else:
            if arg.find(',') == -1: return 'CommaError' 
            elif any([len(prompt[0]) != self.__param_rule[inst][1],
                  len(prompt[1]) != self.__param_rule[inst][2]]): return 'SyntaxError'
            elif len(prompt[0]) == 0 or len(prompt[1]) == 0: return 'TypeError'
            else:
                if any([len(prompt[0]) == 1  and prompt[0] == 'M' and self.check_pointer(prompt[0]),
                        len(prompt[1]) == 1 and prompt[1] == 'M' and self.check_pointer(prompt[0])]
                ): return 'PointerError'

                if any(
                    [len(prompt[0]) == 1 and prompt[0] not in self.__token['register'].keys(),
                     len(prompt[1]) == 1 and prompt[1] not in self.__token['register'].keys()]
                ): return 'RegisterError'
                elif any(
                    [len(prompt[0]) == 5 and prompt[0] not in self.__token['memory'].keys(),
                     len(prompt[1]) == 5 and prompt[1] not in self.__token['memory'].keys()]
                ): return 'MemoryError'
                elif len(prompt[1]) == 3 and prompt[1] not in self.__token['port'].keys(): return 'DataError'
                else: return prompt

    def check_pointer(self,rp:str) -> bool:
        if rp == 'M': rp = 'H'
        if len(self.__rp(rp)) != 5 and self.__rp(rp) in self.__token['port'].keys(): return True
        else: return False