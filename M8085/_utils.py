from random import randbytes
from ._instruction import opcode
from prettytable import PrettyTable

class Setup:
    def memory():
        memory = {}
        for i in range(65536):
            address = hex(i)[2:].upper()
            if len(address) < 4:
                bit = '0'*(4-len(address))
                address = bit + address
            memory[address + 'H'] = '00'
        
        return memory

    def port():
        port = {}
        for i in range(256):
            if len(hex(i)[2:]) == 1 :port['0' + hex(i)[2:].upper() + 'H'] = '0'
            else: port[hex(i)[2:].upper() + 'H'] = '0'
        
        return port

    def register():
        return {'A':'00','B':'00','C':'00','D':'00','E':'00','H':'00','L':'00','M':00,'PC':'0000H','SP':'0000H'}

    def flag():
        return {'S':0,'Z':0,'AC':0,'P':0,'C':0}
        
class Tool:
    TOKEN = None
    PARAM_RULE = {
            'MOV':(2,1,1),
            'MVI':(2,1,3),
            'LXI':(2,1,5),
            'LDA':(1,5),
            'STA':(1,5),
            'LDAX':(1,1),
            'STAX':(1,1),
            'LHLD':(1,5),
            'SHLD':(1,5),
            'XCHG':(0,0),
            'IN':(1,3),
            'OUT':(1,3),
            'ADD':(1,1),
            'ADI':(1,3),
            'ADC':(1,1),
            'SUB':(1,1),
            'SUI':(1,3),
            'SBB':(1,1),
            'SBI':(1,3),
            'INR':(1,1),
            'DCR':(1,1),
            'INX':(1,1),
            'DCX':(1,1),
            'DAD':(1,1),
            'DAA':None,
            'RRC':(0,0),
            'RAR':(0,0),
            'RLC':(0,0),
            'RAL':(0,0),
            'ANI':(1,3),
            'XRI':(1,3),
            'ORI':(1,3),
            'ANA':(1,1),
            'ORA':(1,1),
            'XRA':(1,1),
            'CMA':(0,0),
            'CMP':(1,1),
            'CPI':(1,3),
            'CMC':(0,0),
            'STC':(0,0),
            'PUSH':(1,1),
            'XTHL':(0,0),
            'PCHL':(0,0),
            'SPHL':(0,0),
            'JMP':(1,5),
            'JC':(1,5),
            'JZ':(1,5),
            'JPE':(1,5),
            'JPO':(1,5),
            'JP':(1,5),
            'JM':(1,5),
            'JNZ':(1,5),
            'JNC':(1,5),
            'HLT':(0,0),
            'RST5.5':(0,0),
        }

    def check_param(inst:str,arg:str):
        prompt = arg.upper().replace(' ', '').split(',')
        if inst in ['HLT','RST5.5'] and prompt[0] == '': return ''

        elif Tool.PARAM_RULE[inst][0] == 0 and prompt[0] != '': return 'NoArgumentError'

        elif Tool.PARAM_RULE[inst][0] == 1:
            if len(prompt[0]) != Tool.PARAM_RULE[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in Tool.TOKEN['port'].keys(): return 'DataError'
            elif inst in ['INX','DCX','DAD'] and prompt[0] not in ['H','B','D']: return 'RpError'
            elif inst in ['LDAX', 'STAX'] and prompt[0] == "H": return 'RpNotAllowedError'
            elif inst in ['LDAX', 'STAX'] and prompt[0] not in ['B','D']: return 'RpError'
            else: return prompt[0]
        else:
            if arg.find(',') == -1: return 'CommaError' 
            elif any([len(prompt[0]) != Tool.PARAM_RULE[inst][1],
                  len(prompt[1]) != Tool.PARAM_RULE[inst][2]]): return 'SyntaxError'
            elif len(prompt[0]) == 0 or len(prompt[1]) == 0: return 'TypeError'
            else:
                if any(
                    [len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(),
                     len(prompt[1]) == 1 and prompt[1] not in Tool.TOKEN['register'].keys()]
                ): return 'RegisterError'
                elif any(
                    [len(prompt[0]) == 1 and inst == 'LXI' and prompt[0] not in ['H','B','D'], 
                     len(prompt[1]) == 1 and inst == 'LXI' and prompt[1] not in ['H','B','D']
                    ]
                ): return 'RpError'
                elif any(
                    [len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(),
                     len(prompt[1]) == 5 and prompt[1] not in Tool.TOKEN['memory'].keys()]
                ): return 'MemoryError'
                elif len(prompt[1]) == 3 and prompt[1] not in Tool.TOKEN['port'].keys(): return 'DataError'
                else: return tuple(prompt)
    
    def rp(rp:str = 'H') -> str:
        if rp == 'B': return Tool.TOKEN["register"]['B'] + Tool.TOKEN["register"]['C'] + 'H'
        elif rp == 'D': return  Tool.TOKEN["register"]['D'] + Tool.TOKEN["register"]['E'] + 'H'
        else: return Tool.TOKEN["register"]['H'] + Tool.TOKEN["register"]['L'] + 'H'
    
    def check_parity(result:str):
        if bin(decode(result[:-1])).count('1') % 2 == 0:
            Tool.TOKEN['flag']['P'] = 1
        else:
            Tool.TOKEN['flag']['P'] = 0
        
    def check_zero(result:str):
        if decode(result[:-1]) == 0:
            Tool.TOKEN['flag']['Z'] = 1
        else:
            Tool.TOKEN['flag']['Z'] = 0
    
    def check_sign(result:str):
        if decode(result[:-1]) < 0:
            Tool.TOKEN['flag']['S'] = 1
        else:
            Tool.TOKEN['flag']['S'] = 0

class Memory:
    TOKEN = None

    history = {}
    exe_address = []

    def update_pc(inst:str):
        Memory.TOKEN['register']['PC'] = encode(decode(Memory.TOKEN['register']['PC']) + opcode[inst]['byte'],4)

    def store(bind:tuple):
        key = Memory.TOKEN['register']['PC']
        Memory.history[key] = bind
        Memory.exe_address.append(key)
    
    def fetch():
        key = Memory.TOKEN['register']['PC']
        return Memory.history[key]

    def placement(bind:tuple):
        inst, prompt = bind
        if any([i in opcode[inst] for i in ['H','B', 'D', 'A', 'C', 'E', 'L', 'M']]):
        
            key = prompt[0] if isinstance(prompt, tuple) else prompt

        else:
            if inst == 'MOV':
                key = ','.join(prompt)
            
            else:
                key = 'op'

        address = Memory.TOKEN['register']['PC']
        if opcode[inst]['byte'] == 3:
            if isinstance(prompt ,tuple):
                for i in opcode[inst][key], prompt[1][2:-1], prompt[1][:2]:
                    Memory.TOKEN['stack'][address] = i
                    address = encode(decode(address) + 1,4)
            else:
                for i in opcode[inst][key], prompt[2:-1], prompt[:2]:
                    Memory.TOKEN['stack'][address] = i
                    address = encode(decode(address) + 1,4)
            
        elif opcode[inst]['byte'] == 2:
            if isinstance(prompt ,tuple):
                parse = prompt[1] if len(prompt[1]) == 3 else prompt[0]
            else: parse = prompt
            for i in  opcode[inst][key], parse:
                Memory.TOKEN['stack'][address] = i
                address = encode(decode(address) + 1,4)

        elif opcode[inst]['byte'] == 1:
            Memory.TOKEN['stack'][address] = opcode[inst][key]
            address = encode(decode(address) + 1,4)
        

def get_token():
    return  {
                "memory":Setup.memory(),
                "stack":Setup.memory(),
                "register":Setup.register(),
                "flag":Setup.flag(),
                "port":Setup.port(),
            }

def decode(arg:str, base:int = 16):
    return int(arg.replace('H',''),base)

def encode(arg:int, bit:int=2):
    if bit == 2:
        if len(hex(arg)[2:].upper()) < 2:
            return '0' + hex(arg)[2:].upper() + 'H'

        return hex(arg)[2:].upper() + 'H'
    
    elif bit == 4:
        if len(hex(arg)[2:].upper()) < 4:
            return '0'*(4- len(hex(arg)[2:].upper())) + hex(arg)[2:].upper() + 'H'
        
        return hex(arg)[2:].upper() + 'H'
    