from prettytable import PrettyTable

class Simulator:
    def __init__(self):
        self._memory_address = {hex(i)[2:].upper() + 'H':'0' for i in range(32768,40960)}
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
            'IN':self.__in,
            'OUT':self.__out,
            'ADD':None,
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

    def show(self,exmin:str,address:str):
        if exmin == 'M': return self._memory_address[address]
        
        elif exmin == 'R': return self.__registers[address]

        elif exmin == 'F': return self.__flags[address]
        
        else: return False
    
    def show_memory(self):
        return self._memory_address

    def show_register(self):
        return self.__registers
    
    def show_flag(self):
        return self.__flags

    def __mov(self,rd:str,rs:str):
        if rd in self.__registers.keys():
            if rd == 'M':
                self._memory_address[self.__registers['H'] + self.__registers['L']] =  rs
            elif rs == 'M':
                self.__registers['H'] = rd[:2]
                self.__registers['L'] = rd[2:]
            else:
                self.__registers[rd] = self.__registers[rs]

    def __mvi(self,r:str,data:str):
        if r in self.__registers.keys():
            if r == 'M':
                self._memory_address[self.__registers['H'] + self.__registers['L'] + 'H'] =  data
            else:
                self.__registers[r] = data

    def __lxi(self,rp:str,data:str):
        if rp in self.__registers.keys():
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
        if ma in self._memory_address.keys():
            self.__registers['A'] =  self._memory_address[ma]
    
    def __sta(self, ma:str):
        if ma in self._memory_address.keys():
            self._memory_address[ma] = self.__registers['A']    

    def __ldax(self,rp:str):
        if rp in self.__registers.keys():
            if rp == 'B':
                self.__registers['A'] = self._memory_address[self.__registers['B'] + self.__registers['C'] + 'H']  
            elif rp == 'D':
                self.__registers['A'] = self._memory_address[self.__registers['D'] + self.__registers['E'] + 'H']
    
    def __stax(self,rp:str):
        if rp in self.__registers.keys():
            if rp == 'B':
                self._memory_address[self.__registers['B'] + self.__registers['C'] + 'H'] = self.__registers['A'] 
            elif rp == 'D':
                 self._memory_address[self.__registers['D'] + self.__registers['E'] + 'H'] = self.__registers['A']

    def __lhld(self,ma:str):
        self.__registers['L'] = self._memory_address[ma]
        self.__registers['H'] = self._memory_address[str(int(ma[:-1]) + 1) + 'H']

    def __shld(self,ma:str):
        self._memory_address[ma] = self.__registers['L'] 
        self._memory_address[str(int(ma[:-1]) + 1) + 'H'] = self.__registers['H']
    
    def __in(self,port:str):
        self.__registers['A'] = port
    
    def __out(self,port:str):
        port = self.__registers['A']