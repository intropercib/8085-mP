from . import _utils
from ._data import Data
from ._arithmetic import Arithmetic
from ._logical import Logical
from ._peripheral import Peripheral
from ._branch import Branch
from ._stack import Stack

class Control_Unit:

    def __init__(self):
        self.exe_mode = 0 # 1 -> interpret, 0 -> compile 
        self.__token:dict = _utils.get_token()
        self.__data_inst = Data(self.__token)
        self.__arithmetic_inst = Arithmetic(self.__token)
        self.__logical_inst = Logical(self.__token)
        self.__peripheral_inst = Peripheral(self.__token)
        self.__branch_inst = Branch(self.__token)
        self.__stack_inst = Stack(self.__token)
        _utils.History.TOKEN = _utils.Tool.TOKEN = self.__token

        self.__inst_set = (
            self.__data_inst.get_inst(),
            self.__arithmetic_inst.get_inst(),
            self.__logical_inst.get_inst(),
            self.__peripheral_inst.get_inst(),
            self.__branch_inst.get_inst(),
            self.__stack_inst.get_inst()
        )
    
    def inst_list(self):
        return [_ for _ in _utils.Tool.PARAM_RULE]
    
    def store(self,inst:str,prompt:str=None):
            _utils.History.update((inst, (prompt)))

    def HLT(self):
        while True:
            inst, prompt = _utils.History.fetch()
            if any([inst == 'HLT',inst == 'RST5', inst == prompt == None]):
                _utils.History.TOKEN['stack'] = _utils.Setup.stack()
                _utils.History.history = {}
                _utils.History.TOKEN['register']['SP'] = '7FFFH'
                break
            else:
                for dict in self.__inst_set:
                    for key in dict:
                        if inst == key:
                            if prompt == None:
                                dict[key]()
                            else:
                                dict[key](prompt)            

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