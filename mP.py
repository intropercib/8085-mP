from prettytable import PrettyTable

class Simulator:
    def __init__(self):
        self.__memory_address = {hex(i)[2:].upper() + 'H':'0' for i in range(32768,40960)}
        self.__port = {hex(i)[2:].upper() + 'H':'0' for i in range(256)}
        self.__registers = {'A':'0','B':'0','C':'0','D':'0','E':'0','F':'0','H':'0','L':'0','M':None}
        self.__flags = {'S':0,'Z':0,'AC':0,'P':0,'C':0}
        self.__op_code = {
            'MOV':self.__mov,
            'MVI':self.__mvi,
            'LXI':self.__lxi,
            'LDA':self.__lda,
            'STA':self.__sta,
            'LDAX':self.__ldax,
            'STAX':self.__stax,
            'LHLD':self.__lhld,
            'SHLD':self.__shld,
            'XCHG':self.__xchg,
            'IN':self.__in,
            'OUT':self.__out,
            'ADD':self.__add,
            'ADI':None,
            'ADC':None,
            'SUB':None,
            'SUI':None,
            'SBB':None,
            'SBI':None,
            'INR':None,
            'DCR':None,
            'INX':None,
            'DCX':None,
            'DAD':None,
            'DAA':None
        }

        self.__param_rule = {
            'MOV':(2,1,1),
            'MVI':(2,1,3),
            'LXI':(2,1,5),
            'LDA':(1,5),
            'STA':(1,5),
            'LDAX':(1,1),
            'STAX':(1,1),
            'LHLD':(1,5),
            'SHLD':(1,5),
            'XCHG':(0,1),
            'IN':(1,3),
            'OUT':(1,3),
            'ADD':(1,1),
            'ADI':None,
            'ADC':None,
            'SUB':None,
            'SUI':None,
            'SBB':None,
            'SBI':None,
            'INR':None,
            'DCR':None,
            'INX':None,
            'DCX':None,
            'DAD':None,
            'DAA':None
        }
    
    def op_code(self,code:str):
        return self.__op_code[code]
    
    def param(self):return self.__param_rule

    def show(self,exmin:str,address:str):
        if exmin == 'M': return self.__memory_address[address]
        
        elif exmin == 'R': return self.__registers[address]

        elif exmin == 'F': return self.__flags[address]

        elif exmin == 'P': return self.__port[address]
        
        else: return False
    
    def show_memory(self):
        return self.__memory_address

    def show_register(self):
        return self.__registers
    
    def show_flag(self):
        return self.__flags
    
    def show_port(self):
        return self.__port

    def __mov(self,rd:str,rs:str):
        if rd == 'M':
            if self.__registers['H'] + self.__registers['L'] + 'H' in self.__memory_address:
                self.__memory_address[self.__registers['H'] + self.__registers['L'] + 'H'] =  rs
        elif rs == 'M':
            self.__registers['H'] = rd[:2]
            self.__registers['L'] = rd[2:]
        else:
            self.__registers[rd] = self.__registers[rs]

    def __mvi(self,r:str,data:str):
        if r == 'M':
            if self.__registers['H'] + self.__registers['L'] + 'H' in self.__memory_address:
                self.__memory_address[self.__registers['H'] + self.__registers['L'] + 'H'] =  data
        else:
            self.__registers[r] = data

    def __lxi(self,rp:str,data:str):
        if rp == 'B':
            self.__registers[rp] = data[:2]
            self.__registers['C'] = data[2:-1]
        
        elif rp == 'D':
            self.__registers[rp] = data[:2]
            self.__registers['E'] = data[2:-1]
        
        elif rp == 'H':
            self.__registers[rp] = data[:2]
            self.__registers['L'] = data[2:-1]

    def __lda(self,ma:str):
        self.__registers['A'] =  self.__memory_address[ma]
    
    def __sta(self, ma:str):
        self.__memory_address[ma] = self.__registers['A']    

    def __ldax(self,rp:str):
        if rp == 'B':
            self.__registers['A'] = self.__memory_address[self.__registers['B'] + self.__registers['C'] + 'H']  
        elif rp == 'D':
            self.__registers['A'] = self.__memory_address[self.__registers['D'] + self.__registers['E'] + 'H']
    
    def __stax(self,rp:str):
        if rp == 'B':
            self.__memory_address[self.__registers['B'] + self.__registers['C'] + 'H'] = self.__registers['A'] 
        elif rp == 'D':
                self.__memory_address[self.__registers['D'] + self.__registers['E'] + 'H'] = self.__registers['A']

    def __lhld(self,ma:str):
        self.__registers['L'] = self.__memory_address[ma]
        self.__registers['H'] = self.__memory_address[str(int(ma[:-1]) + 1) + 'H']

    def __shld(self,ma:str):
        self.__memory_address[ma] = self.__registers['L'] 
        self.__memory_address[str(int(ma[:-1]) + 1) + 'H'] = self.__registers['H']
    
    def __xchg(self):
        self.__registers['D'],self.__registers['H'] = self.__registers['H'],self.__registers['D']
        self.__registers['E'],self.__registers['L'] = self.__registers['L'],self.__registers['E']
    
    def __in(self,port:str):
        self.__registers['A'] = port
    
    def __out(self,port:str):
        self.__port[port] = self.__registers['A']
    
    def __add(self,r:str):
        self.__registers['A'] = hex(int(self.__registers['A'].replace('H',''),16) +  int(self.__registers[r].replace('H',''),16))[2:].upper() + 'H'
