from ._utils import encode, decode, INSTRUCTION

_MEMORY = {}
_STACK = {}
_REGISTER = {
    'A':'00H','B':'90H','C':'00H','D':'00H','E':'00H','H':'00H','L':'00H','M':'00H',
    'PC':'0000H','SP':'0000H'
}
_FLAG = {'S':0,'Z':0,'AC':0,'P':0,'C':0}

class Memory:

    def __getitem__(self,address):
        if address in _MEMORY: return _MEMORY[address]
        else: return '00H'

    def __setitem__(self,address, data):
        if data == '00H':
            if address in _MEMORY: _MEMORY.pop(address, None)
        else:
            _MEMORY[address] = data

    def write(self,address, data):
        if data == '00H':
            if address in _MEMORY: _MEMORY.pop(address, None)
        else:
            _MEMORY[address] = data

    def read(self,address):
        if address in _MEMORY: return _MEMORY[address]
    
    def get_used_addresses(self):
        return _MEMORY.keys()
    
    def reset(self):
        _MEMORY.clear()
    

class Register:

    def __getitem__(self,register):
        if register in _REGISTER: return _REGISTER[register]
        else: raise KeyError(f"Register {register} not found.")
    
    def __setitem__(self,register, data):
        self.write(register, data)

    def write(self,register, data):
        if register in _REGISTER:
            _REGISTER[register] = data
    
    def read(self,register):
        if register in _REGISTER:
            return _REGISTER[register]

    def get_all(self):
        return _REGISTER
    
    def reset(self):
        for reg in _REGISTER:
            if reg in ['PC', 'SP']:
                _REGISTER[reg] = '0000H'
            else:
                _REGISTER[reg] = '00H'

class Flag:

    def __getitem__(self,flag):
        if flag in _FLAG: return _FLAG[flag]
        else: raise KeyError(f"Flag {flag} not found.")

    def __setitem__(self,flag, value):
        self.set(flag, value)

    def set(self,flag, value):
        if flag in _FLAG:
            _FLAG[flag] = 1 if value else 0
    
    def get(self,flag):
        if flag in _FLAG:
            return _FLAG[flag]
    
    def get_all(self):
        return _FLAG
    
    def reset(self):
        for flag in _FLAG:
            _FLAG[flag] = 0

class Assembler:

    def pass1(self, line:dict):

        pc = _REGISTER['PC']
        
        if 'label' in line:
            label = line['label']
            _STACK[label] = pc

        if 'code' in line:
            inst = line['inst']
            code = line['code']
            inr = INSTRUCTION[inst]['byte']

            _STACK[pc] = code
            _REGISTER['PC'] = encode(decode(pc) + inr, bit =4)
        
    def pass2(self):
        for pc, code in _STACK.items():
            if not isinstance(code, list):
                continue
            inst = code[0]
            if INSTRUCTION[inst]['param_rule'] == ['l']:
                label = code[1]
                if label not in _STACK:
                    self.reset()
                    return f'Subroutine {label} not defined'
                code[1] = _STACK[label]
                _STACK[pc] = code

        self.reset_pc()

    def reset(self):
        _STACK.clear()
        self.reset_pc()
    
    def reset_pc(self):
        _REGISTER['PC'] = '0000H'

def decode_rp(rp:str = 'H') -> str:
    if rp == 'B': return _REGISTER['B'] + _REGISTER['C'] + 'H'
    elif rp == 'D': return  _REGISTER['D'] + _REGISTER['E'] + 'H'
    else: return _REGISTER['H'] + _REGISTER['L'] + 'H'

def check_parity(result:str):
    if bin(decode(result)).count('1') % 2 == 0:
        _FLAG['P'] = 1
    else:
        _FLAG['P'] = 0
    
def check_zero(result:str):
    if decode(result) == 0:
        _FLAG['Z'] = 1
    else:
        _FLAG['Z'] = 0

def check_sign(result:str):
    if decode(result) < 0:
        _FLAG['S'] = 1
    else:
        _FLAG['S'] = 0