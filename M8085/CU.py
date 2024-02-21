from . import _utils
from ._instruction import opcode
from ._data import Data
from ._arithmetic import Arithmetic
from ._logical import Logical
from ._peripheral import Peripheral
from ._branch import Branch
from ._stack import Stack

from prettytable import PrettyTable

class Control_Unit:

    def __init__(self,token):
        self.mode = 1# 1 -> interpret, 0 -> compile 
        self.__token:dict = token
        self.__data_inst = Data(self.__token)
        self.__arithmetic_inst = Arithmetic(self.__token)
        self.__logical_inst = Logical(self.__token)
        self.__peripheral_inst = Peripheral(self.__token)
        self.__branch_inst = Branch(self.__token)
        self.__stack_inst = Stack(self.__token)
        _utils.Memory.TOKEN = self.__token

        self.__token['register']['PC'] = '0000H'

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
    
    def cycle(self,inst:str,prompt=None):
        bind = (inst, (prompt))
        _utils.Memory.store(bind)
        _utils.Memory.placement(bind)

        if inst in self.__branch_inst.get_inst():
            self.mode = 0

        if self.mode:
            self.__bit_wise(inst,prompt)
        
        elif not self.mode:
            if inst == 'HLT':
                self.__compile()
            _utils.Memory.update_pc(inst)            

    def __bit_wise(self,inst:str,prompt:str=None):
            self.__exe(inst,prompt)
            _utils.Memory.update_pc(inst)

    def __compile(self):
        for key in _utils.Memory.exe_address:
            inst,prompt = _utils.Memory.history[key]
            if any([inst == 'HLT',inst == 'RST5']):
                break
            self.__exe(inst,prompt)

    def reset(self):
        _utils.Memory.history = {}
        _utils.Memory.exe_address = []
        _utils.Memory.TOKEN['register']['PC'] = '0000H'

    def __exe(self, inst, prompt):
        for dict in self.__inst_set:
            for key in dict:
                if inst == key:
                    if prompt == None:
                        dict[key]()
                    else:
                        dict[key](prompt)

    def assemble(self):
        assemble_table = PrettyTable(['Address','Mnemonics','Bytes','Op Code', 'Data'])
        for address in _utils.Memory.TOKEN['stack']:
            
            if address == _utils.Memory.TOKEN['register']['PC']:
                break

            mnemonics = op_code = byte = data ='-'
            if address in _utils.Memory.exe_address:
                inst,prompt = _utils.Memory.history[address]
                if isinstance(prompt, tuple):
                    prompt = ','.join(prompt)
                mnemonics = ' '.join([inst,prompt])
                op_code = _utils.Memory.TOKEN['stack'][address]
                byte = opcode[inst]['byte']

            else:
                data = _utils.Memory.TOKEN['stack'][address]

            assemble_table.add_row(
                (address,mnemonics,byte,op_code, data)
            )
            
        return assemble_table          

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