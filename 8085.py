class Simulator:
    def __init__(self):
        self.__memory_address = {hex(i)[2:] + 'H':'0' for i in range(32768,40960)}
        self.__registers = {'A':'0','B':'0','C':'0','D':'0','E':'0','F':'0','H':'0','L':'0','M':None}
        self.__flags = {'S':0,'Z':0,'A':0,'P':0,'C':0}
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
            'IN':None,
            'OUT':None,
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

    def show(self,exmin:str,address:str):
        if exmin == 'M':
            return self.__memory_address[address]
        elif exmin == 'R':
            return self.__registers[address]
        else:
            return False

    def __mov(self,rd:str,rs:str):
        if rd in self.__registers.keys():
            if rd == 'M':
                self.__memory_address[self.__registers['H'] + self.__registers['L']] =  rs
            elif rs == 'M':
                self.__registers['H'] = rd[:2]
                self.__registers['L'] = rd[2:]
            else:
                self.__registers[rd] = rs

    def __mvi(self,r:str,data:str):
        if r in self.__registers.keys():
            if r == 'M':
                self.__memory_address[self.__registers['H'] + self.__registers['L']] =  data
            else:
                self.__memory_address[r] = data

    def __lxi(self,rp:str,data:str):
        if rp in self.__registers.keys():
            if rp == 'B':
                self.__registers[rp] = data[:2]
                self.__registers['C'] = data[2:]
            
            elif rp == 'D':
                self.__registers[rp] = data[:2]
                self.__registers['E'] = data[2:]
            
            elif rp == 'H':
                self.__registers[rp] = data[:2]
                self.__registers['L'] = data[2:]

    def __lda(self,ma:str):
        if ma in self.__memory_address.keys():
            self.__registers['A'] =  self.__memory_address[hex(ma)]

    def __ldax(self,rp:str):
        if rp in self.__registers.keys():
            if rp == 'B':
                self.__registers['A'] = self.__memory_address[self.__registers['B'] + self.__registers['C']]  
            elif rp == 'D':
                self.__registers['A'] = self.__memory_address[self.__registers['D'] + self.__registers['E']]
    
    def __stax(self,rp:str):
        if rp in self.__registers.keys():
            if rp == 'B':
                self.__memory_address[self.__registers['B'] + self.__registers['C']] = self.__registers['A'] 
            elif rp == 'D':
                 self.__memory_address[self.__registers['D'] + self.__registers['E']] = self.__registers['A']

    def __lhld(self,ma:str):
        self.__registers['H'] = self.__memory_address[ma]
        self.__registers['L'] = self.__memory_address[hex(int(ma, 16) + 1)]

    def __shld(self,ma:str):
        self.__memory_address[ma] = self.__registers['H'] 
        self.__memory_address[hex(int(ma, 16) + 1)] = self.__registers['L']

    def __sta(self, ma:str):
        if ma in self.__memory_address.keys():
            self.__memory_address[ma] = self.__registers['A']