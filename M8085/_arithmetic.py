from ._base import Instruction
from ._utils import encode, decode
from ._memory import Memory, Register, Flag, decode_rp, check_parity, check_sign, check_zero

class Arithmetic(Instruction):

    def __init__(self):
        self._memory:Memory = Memory()
        self._register:Register = Register()
        self._flag:Flag = Flag()

    def __add(self,r:str):
        if r == 'M':
            self._register['A'] = encode( decode(self._register['A']) +  decode( self._memory.read(decode_rp()) ) )
        else:
            self._register['A'] = encode( decode(self._register['A']) +  decode(self._register.read(r)) )
        
        if len(self._register['A']) > 3:
            self._flag['C'] = 1
            self._register['A'] = self._register['A'][1:]
        
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 
        check_sign(self._register['A']) 

    def __adc(self,r:str):
        if r == 'M':
            self._register['A'] = encode( decode(self._register['A']) +  decode(self._memory[decode_rp()]) + self._flag['C'] )
        else:
            self._register['A'] = encode( decode(self._register['A']) + decode(self._register[r]) + self._flag['C'] )

        if len(self._register['A']) > 3:
            self._flag['C'] = 1
            self._register['A'] = self._register['A'][1:]

        check_parity(self._register['A'])
        check_zero(self._register['A'])         
        check_sign(self._register['A'])         
        
    def __adi(self,data:str):
        self._register['A'] = encode(decode(self._register['A']) +  decode(data))

        if len(self._register['A']) > 3:
            self._flag['C'] = 1
            self._register['A'] = self._register['A'][1:]
        
        check_parity(self._register['A'])  
        check_zero(self._register['A']) 
        check_sign(self._register['A']) 
    
    def __dad(self,rp:str):
        self._memory[decode_rp()] = encode(decode(self._memory[decode_rp()]) +  decode(self._memory[decode_rp(rp)]))

        if len(self._memory[decode_rp()]) > 3:
            self._flag['C'] = 1
            self._memory[decode_rp()] = self._memory[decode_rp()][1:]
        
        check_parity(self._memory[decode_rp()]) 
        check_zero(self._memory[decode_rp()])  
        check_sign(self._memory[decode_rp()])  

    def __sub(self,r:str):

        if r == 'M':
            if decode(self._memory[decode_rp()]) > decode(self._register['A']):
                self._flag['C'] = 1  
            self._register['A'] = encode( abs(decode(self._register['A'] -  decode(self._memory[decode_rp()]))) )
        else:
            if decode(self._register[r]) > decode(self._register['A']):
                self._flag['C'] = 1
            self._register['A'] = encode( abs(decode(self._register['A']) -  decode(self._register[r])) )
        
            check_parity(self._register['A'])  
            check_zero(self._register['A'])  
            check_sign(self._register['A'])  

    def __sbb(self,r:str):

        if r == 'M':
            if decode(self._memory[decode_rp()]) + self._flag['C'] > decode(self._register['A']):
                self._flag['C'] = 1
            self._register['A'] = encode( decode(self._register['A']) - ( decode(self._memory[decode_rp()]) + self._flag['C'] ) )
        else:
            if decode(self._register[r]) + self._flag['C'] > decode(self._register['A']):
                self._flag['C'] = 1
            self._register['A'] = encode( decode(self._register['A']) - ( decode(self._register[r]) + self._flag['C'] ) )
        
            check_parity(self._register['A'])  
            check_zero(self._register['A'])  
            check_sign(self._register['A'])  

    def __sui(self,data:str):
        if decode(data) > decode(self._register['A']):
            self._flag['C'] = 1
        self._register['A'] = encode(decode(self._register['A']) -  decode(data))

        check_parity(self._register['A'])  
        check_zero(self._register['A'])  
        check_sign(self._register['A'])  
    
    def __sbi(self,data:str):
        rawDat = decode(data)
        idat = ((~rawDat + 1) & ((1 << len( bin(rawDat)[2:]) ) - 1)) #2's complement
        if idat + self._flag['C'] > decode(self._register['A']):
            self._flag['C'] = 1
        self._register['A'] = encode(decode(self._register['A']) - ( idat + self._flag['C'] ))

        check_parity(self._register['A'])
        check_zero(self._register['A']) 
        check_sign(self._register['A']) 

    def __inr(self,r:str):

        if r == 'M':
            new = encode(decode(decode_rp().replace('H','')) + 1)[:-1]
            self._register['H']  = new[:2]
            self._register['L']  = new[2:]
            check_parity(new)
            check_zero(new)
            check_sign(new)

        else:
            self._register[r] = encode( decode(self._register[r]) + 1 )
            check_parity(self._register[r])
            check_zero(self._register[r])
            check_sign(self._register[r])
    
    def __inx(self,rp:str):
        self._memory[decode_rp(rp)] = encode(decode(self._memory[decode_rp(rp)]) + 1)
             
    def __dcx(self,rp:str):
        self._memory[decode_rp(rp)] = encode(decode( self._memory[decode_rp(rp)] ) - 1 ) 
    
    def __dcr(self,r:str):

        if r == 'M':
            new = encode(decode(decode_rp().replace('H','')) - 1)[:-1]
            self._register['H']  = new[:2]
            self._register['L']  = new[2:]
            check_parity(new)
            check_zero(new)
            check_sign(new)
        else:
            self._register[r] = encode( decode(self._register[r]) - 1 )
            check_parity(self._register[r])
            check_zero(self._register[r]) 
            check_sign(self._register[r])

    def __daa(self,*args): 
        return 'Not Implemented Yet'

    def get_inst(self):
        return {
            'ADD':self.__add,
            'ADI':self.__adi,
            'ADC':self.__adc,
            'SUB':self.__sub,
            'SUI':self.__sui,
            'SBB':self.__sbb,
            'SBI':self.__sbi,
            'INR':self.__inr,
            'DCR':self.__dcr,
            'INX':self.__inx,
            'DCX':self.__dcx,
            'DAD':self.__dad,
            'DAA':self.__daa,
            'INR':self.__inr,
            'INX':self.__inx,
            'DCR':self.__dcr,
            'DCX':self.__dcx,
        }    
