from ._utils import decode,encode,Tool
class Logical:

    def __init__(self, token:dict):
        Tool.TOKEN = token
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']

    def __rrc(self):
        accumulator_value = bin(decode(self.__register['A']))[2:].zfill(8)
        self.__flag['C'] = int(accumulator_value[-1])
        rotated_value = accumulator_value[-1] + accumulator_value[:-1]
        self.__register['A'] = encode(int(rotated_value,2))
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __rar(self):
        accumulator_value = bin(decode(self.__register['A']))[2:].zfill(8)
        rotated_value = str(self.__flag['C']) + accumulator_value[:-1]
        self.__flag['C'] = int(accumulator_value[-1])
        self.__register['A'] = encode(int(rotated_value,2))
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __rlc(self):
        accumulator_value = bin(decode(self.__register['A']))[2:].zfill(8)
        rotated_value = accumulator_value[1:] + accumulator_value[0]
        self.__flag['C'] = int(accumulator_value[0])
        self.__register['A'] = encode(int(rotated_value,2))
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __ral(self):
        accumulator_value = bin(decode(self.__register['A']))[2:].zfill(8)
        rotated_value = accumulator_value[1:] + str(self.__flag['C'])
        self.__flag['C'] = decode(accumulator_value[0],2)
        self.__register['A'] = encode(decode(rotated_value,2))
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 
        
    def __ani(self, arg: list):
        self.__register['A'] = encode(decode(self.__register['A']) & decode(arg[0]))
        self.__flag['C'], self.__flag['AC'] = 0, 1
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __xri(self, arg: list):
        self.__register['A'] = encode(decode(self.__register['A']) ^ decode(arg[0]))
        self.__flag['C'], self.__flag['AC'] = 0, 0

    def __ori(self, arg: list):
        self.__register['A'] = encode(decode(self.__register['A']) | decode(arg[0]))
        self.__flag['C'], self.__flag['AC'] = 0, 0
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __ana(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode(decode(self.__register['A']) & decode(self.__memory_address[Tool.rp()]))
        else:
            self.__register['A'] = encode(decode(self.__register['A']) & decode(self.__register[r]))
        self.__register['AC'], self.__register['C'] = 1, 0
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 

    def __ora(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode(decode(self.__register['A']) | decode(self.__memory_address[Tool.rp()]))
        else:
            self.__register['A'] = encode(decode(self.__register['A']) | decode(self.__register[r]))
        self.__register['AC'], self.__register['C'] = 0, 0
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A'])

    def __xra(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode(decode(self.__register['A']) ^ decode(self.__memory_address[Tool.rp()]))
        else:
            self.__register['A'] = encode(decode(self.__register['A']) ^ decode(self.__register[r]))
        self.__register['AC'], self.__register['C'] = 0, 0
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 
    
    def __cma(self):
        self.__registers['A'] = encode(~decode(self.__registers['A']) & 0xFF)

    def __cmp(self, arg: list):
        a_value = decode(self.__register['A'])
        if arg[0] == "M":
            data_value = decode(self.__memory_address[Tool.rp()])
        else:
            data_value = decode(self.__register[arg[0]])
        if a_value < data_value:
            self.__flag['C'], self.__flag['Z'] = 1, 0
        elif a_value == data_value:
            self.__flag['C'], self.__flag['Z'] = 0, 1
        else:
            self.__flag['C'], self.__flag['Z'] = 0, 0
    
    def __cpi(self, arg: list):
        a_value = decode(self.__register['A'])
        data_value = decode(arg[0])
        if a_value < data_value:
            self.__flag['C'], self.__flag['Z'] = 1, 0
        elif a_value == data_value:
            self.__flag['C'], self.__flag['Z'] = 0, 1
        else:
            self.__flag['C'], self.__flag['Z'] = 0, 0
    
    def __cmc(self):
        self.__flag['C'] = encode(not self.__flag['C'], 'bool')

    def __stc(self):
        self.__flag['C'] = 1
    
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