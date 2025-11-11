from ._parser import Parser
from ._utils import decode, encode
from ._arithmetic import Arithmetic
from ._data import Data
from ._logical import Logical
from ._peripheral import Peripheral
from ._stack import Stack
from ._timing import TimingDiagram
from ._memory import Memory, Register, Flag

class Processor:

    def __init__(self,instruction:str):

        self.__arithmetic = Arithmetic()
        self.__data = Data()
        self.__logical = Logical()
        self.__peripheral = Peripheral()
        self.__stack = Stack()
        self.__parser = Parser(instruction)
        self.__timing = TimingDiagram()
        self.__input = instruction
        self.inst = {}
        self.__inst_set()

    def __inst_set(self):
        for inst in [
            self.__arithmetic,
            self.__data,
            self.__logical,
            self.__peripheral,
            self.__stack
        ]:
            self.inst.update(inst.get_inst())

    @property
    def input(self):
        return self.__input
    
    def exec(self, instr_list:list):
        for inst in instr_list:
            mnemonic, operands = inst[0], inst[1:]

            if mnemonic == 'HLT':
                return 'HLT'

            if mnemonic == 'CALL':
                return mnemonic

            if mnemonic == 'RET':
                return 'RET'

            if operands == []:
                try:
                    self.inst[mnemonic]()
                except KeyError:
                    pass
            else:
                try:
                    self.inst[mnemonic](*operands)
                except KeyError:
                    pass
        
        return 0
            
    def run(self):
        struct = self.__parser.structure

        if isinstance(struct, str):
            return struct

        labels = list(struct.keys())
        prev_label = 'START'
        output = 0

        while True:
            if not output:
                label = labels.pop(0)

            stack = struct[label]

            output = self.exec(stack)

            if output == 'HLT':
                break

            if output:
                if output == 'RET':
                    label = prev_label
                
                else:
                    prev_label, label = label, output