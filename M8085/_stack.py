from ._base import Instruction
from ._utils import encode,decode
from ._memory import Memory, Register

class Stack(Instruction):
    def __init__(self):
        self._stack:Memory = Memory()
        self._register:Register = Register()

    def __push(self, rp:str):
        if rp == 'B':
            self._stack[self._register['SP']] = self._register['B']  + self._register['C']

        elif rp == 'D':
            self._stack[self._register['SP']] = self._register['D']  + self._register['E']

        elif rp == 'H':
            self._stack[self._register['SP']] = self._register['H']  + self._register['L']

        self._register['SP'] = encode(decode(self._register['SP'])-1)

    def __pop(self,rp:str):
        self._register['SP'] = encode(decode(self._register['SP'])+1)
        if rp == 'B':
            self._register['B'] = self._register['SP'][:2] 
            self._register['C'] = self._register['SP'][2:]

        elif rp == 'D':
            self._register['D'] = self._register['SP'][:2] 
            self._register['E'] = self._register['SP'][2:]

        elif rp == 'H':
            self._register['H'] = self._register['SP'][:2] 
            self._register['L'] = self._register['SP'][2:]

        self._register['SP'] = encode(decode(self._register['SP'])+1)

    def __xthl(self):
        data = self._register['H'] + self._register['L']
        data, self._stack['SP'] = self._stack['SP'], data

        self._register['H'] = data[:2]
        self._register['L'] = data[2:]

    def __sphl(self):
        self._register['SP'] = self._register['H'] + self._register['L']
    
    def __pchl(self):
        self._register['PC'] = self._register['H'] + self._register['L']
    
    def __hlt(self):
        pass
    
    __rst55 = __hlt

    def get_inst(self):
        return {
            "PUSH": self.__push,
            "POP": self.__pop,
            "XTHL": self.__xthl,
            "SPHL": self.__sphl,
            "PCHL": self.__pchl,
            "HLT":self.__hlt,
            "RST5.5": Stack.__rst55
        }

