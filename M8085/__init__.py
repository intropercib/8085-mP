from ._parser import Parser, Message
from ._utils import decode, encode, INSTRUCTION
from ._arithmetic import Arithmetic
from ._data import Data
from ._logical import Logical
from ._peripheral import Peripheral
from ._stack import Stack
from ._branch import Branch
from ._timing import TimingDiagram
from ._memory import Memory, Register, Flag, Assembler, _STACK
from .logs import setup_logger, info

RUNTIME = 1000
setup_logger()

class Processor:

    def __init__(self,input:str):

        self.__arithmetic = Arithmetic()
        self.__data = Data()
        self.__logical = Logical()
        self.__peripheral = Peripheral()
        self.__stack = Stack()
        self.__branch = Branch()
        self.__parser = Parser(input)
        self.__timing = TimingDiagram()
        self.__pc = Assembler()
        self.__register = Register()
        self.__input = input
        self.inst = {}
        self.__inst_set()

        self.__rt = 0

    def __inst_set(self):
        for inst in [
            self.__arithmetic,
            self.__branch,
            self.__data,
            self.__logical,
            self.__peripheral,
            self.__stack
        ]:
            self.inst.update(inst.get_inst())

    @property
    def input(self):
        return self.__input
    
    def execute(self):

        result = self.__parser.parse()

        if isinstance(result, Message):
            return result

        result = self.__pc.pass2()

        if isinstance(result, str):
            return result
        
        
        while True:
            
            
            if self.__rt > RUNTIME:
                return "Runtime exceeded"

            pc = self.__register['PC']

            inst , *code = _STACK[pc]

            if inst == 'HLT':
                break

            self.inst[inst]( *code )

            if isinstance(self.inst[inst].__self__, Branch):
                self.__rt += 1
                info(f"{pc} {inst} {code}")
                continue

            else:
                inr = INSTRUCTION[inst]['byte']
                self.__register['PC'] = encode (decode(self.__register['PC']) + inr, 4)
                info(f"{pc} {inst} {code}")
                self.__rt += 1
        
            # try: # Handle No Return cases
            #     pc = self.__register['PC']
            #     inst , *code = _STACK[pc]
            #     info(f"{pc} {inst} {code}")
            #     return 'Infinte Loop Detected'
            
            # except KeyError:
            #     break

            # else:
            #     inst , *code = _STACK[pc]

            #     if inst == 'HLT':
            #         break

            #     self.inst[inst]( *code )

            #     if isinstance(self.inst[inst].__self__, Branch):
            #         continue

            #     else:
            #         inr = INSTRUCTION[inst]['byte']
            #         self.__register['PC'] = encode (decode(self.__register['PC']) + inr, 4)
            #         print(self.__register['PC'])
                
            #     self.__rt += 1
            
            # info(f"{pc} {inst} {code}")
        
        self.__rt = 0