from ._base import Instruction
from ._utils import decode,encode
from ._memory import Memory,Register,Flag, check_zero,check_parity

class Logical(Instruction):

    def __init__(self):
        self._memory:Memory = Memory()
        self._register:Register = Register()
        self._flag:Flag = Flag()

    def __rrc(self):
        accumulator_value = bin(decode(self._register['A']))[2:].zfill(8)
        self._flag['C'] = int(accumulator_value[-1])
        rotated_value = accumulator_value[-1] + accumulator_value[:-1]
        self._register['A'] = encode(int(rotated_value,2))
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __rar(self):
        accumulator_value = bin(decode(self._register['A']))[2:].zfill(8)
        rotated_value = str(self._flag['C']) + accumulator_value[:-1]
        self._flag['C'] = int(accumulator_value[-1])
        self._register['A'] = encode(int(rotated_value,2))
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __rlc(self):
        accumulator_value = bin(decode(self._register['A']))[2:].zfill(8)
        rotated_value = accumulator_value[1:] + accumulator_value[0]
        self._flag['C'] = int(accumulator_value[0])
        self._register['A'] = encode(int(rotated_value,2))
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __ral(self):
        accumulator_value = bin(decode(self._register['A']))[2:].zfill(8)
        rotated_value = accumulator_value[1:] + str(self._flag['C'])
        self._flag['C'] = decode(accumulator_value[0],2)
        self._register['A'] = encode(decode(rotated_value,2))
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 
        
    def __ani(self, data:str):
        self._register['A'] = encode(decode(self._register['A']) & decode(data))
        self._flag['C'], self._flag['AC'] = 0, 1
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __xri(self, data:str):
        self._register['A'] = encode(decode(self._register['A']) ^ decode(data))
        self._flag['C'], self._flag['AC'] = 0, 0

    def __ori(self, data:str):
        self._register['A'] = encode(decode(self._register['A']) | decode(data))
        self._flag['C'], self._flag['AC'] = 0, 0
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __ana(self, r:str):
        if r == 'M':
            self._register['A'] = encode(decode(self._register['A']) & decode(self._memory[Memory()]))
        else:
            self._register['A'] = encode(decode(self._register['A']) & decode(self._register[r]))
        self._register['AC'], self._register['C'] = 1, 0
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __ora(self, r:str):
        if r == 'M':
            self._register['A'] = encode(decode(self._register['A']) | decode(self._memory[Memory()]))
        else:
            self._register['A'] = encode(decode(self._register['A']) | decode(self._register[r]))
        self._register['AC'], self._register['C'] = 0, 0
        check_parity(self._register['A']) 
        check_zero(self._register['A'])

    def __xra(self, r:str):
        if r == 'M':
            self._register['A'] = encode(decode(self._register['A']) ^ decode(self._memory[Memory()]))
        else:
            self._register['A'] = encode(decode(self._register['A']) ^ decode(self._register[r]))
        self._register['AC'], self._register['C'] = 0, 0
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 
    
    def __cma(self):
        self.__registers['A'] = encode(~decode(self.__registers['A']) & 0xFF)

    def __cmp(self, r:str):
        a_value = decode(self._register['A'])
        if r == "M":
            data_value = decode(self._memory[Memory()])
        else:
            data_value = decode(self._register[r])
        if a_value < data_value:
            self._flag['C'], self._flag['Z'] = 1, 0
        elif a_value == data_value:
            self._flag['C'], self._flag['Z'] = 0, 1
        else:
            self._flag['C'], self._flag['Z'] = 0, 0
    
    def __cpi(self, data:str):
        a_value = decode(self._register['A'])
        data_value = decode(data)
        if a_value < data_value:
            self._flag['C'], self._flag['Z'] = 1, 0
        elif a_value == data_value:
            self._flag['C'], self._flag['Z'] = 0, 1
        else:
            self._flag['C'], self._flag['Z'] = 0, 0
    
    def __cmc(self):
        self._flag['C'] = encode(not self._flag['C'], 'bool')

    def __stc(self):
        self._flag['C'] = 1
    
    def get_inst(self):
        return {
            'RRC':self.__rrc,
            'RAR':self.__rar,
            'RLC':self.__rlc,
            'RAL':self.__ral,
            'ANI':self.__ani,
            'XRI':self.__xri,
            'ORI':self.__ori,
            'ANA':self.__ana,
            'ORA':self.__ora,
            'XRA':self.__xra,
            'CMA':self.__cma,
            'CMP':self.__cmp,
            'CPI':self.__cpi,
            'CMC':self.__cmc,
            'STC':self.__stc
        }