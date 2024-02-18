from random import randbytes

class Setup:
    def memory():
        return {hex(i)[2:].upper() + 'H':'0' for i in range(32768,40960)}


    def port():
        port = {}
        for i in range(256):
            if len(hex(i)[2:]) == 1 :port['0' + hex(i)[2:].upper() + 'H'] = '0'
            else: port[hex(i)[2:].upper() + 'H'] = '0'
        
        return port

    def register():
        return {'A':'0','B':'0','C':'0','D':'0','E':'0','H':'0','L':'0','M':0,'PC':'0','SP':'7FFFH'}

    def flag():
        return {'S':0,'Z':0,'AC':0,'P':0,'C':0}
    
    def stack():
        return {hex(i)[2:].upper() + 'H':'0' for i in range(20480,32768)}
    
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
        if inst in ['HLT','RST5.5'] and prompt[0] == '': return inst

        elif Tool.PARAM_RULE[inst][0] == 0 and prompt[0] != '': return 'NoArgumentError'

        elif Tool.PARAM_RULE[inst][0] == 1:
            if len(prompt[0]) != Tool.PARAM_RULE[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in Tool.TOKEN['port'].keys(): return 'DataError'
            elif inst in ['LDAX','STAX','INX','DCX','DAD']: 
                if prompt[0] not in ['H','B','D']: return 'RpError'
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
        if len( [_ for _ in bin(decode(result[:-1]))[1:] if _ == '1'] ) % 2 == 0:
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

class History:
    
    TOKEN = None

    history = {}

    def code_address():
        total = 0
        address = ''
        while any([len(address) != 5, address in History.history]):
            for i in randbytes(5):
                total += i * 10
                address = hex(total).upper()[2:] + 'H'
        else:
            return address
    
    def update(bind:tuple):
        code_address = History.code_address()
        stack = History.TOKEN['stack']
        stack_pointer = History.TOKEN['register']['SP']

        History.history[code_address] = bind
        stack[stack_pointer] = code_address
        History.TOKEN['register']['SP'] = encode(decode(stack_pointer) - 1)
    
    def fetch():
        if History.TOKEN['register']['SP'] != '7FFFH':
            History.TOKEN['register']['SP'] = encode(decode(History.TOKEN['register']['SP']) + 1)
            stack_pointer = History.TOKEN['register']['SP']
            code_address = History.TOKEN['stack'][stack_pointer]
            History.TOKEN['register']['PC'] = code_address
            return History.history[code_address]
        else:
            return None,None #inst, param

def get_token():
    return  {
                "memory":Setup.memory(),
                "stack":Setup.stack(),
                "register":Setup.register(),
                "flag":Setup.flag(),
                "port":Setup.port(),
            }

def decode(arg:str, base:int = 16):
    return int(arg.replace('H',''),base)

def encode(arg:int):
    if len(hex(arg)[2:].upper()) < 2:
        return '0' + hex(arg)[2:].upper() + 'H'
    
    return hex(arg)[2:].upper() + 'H'