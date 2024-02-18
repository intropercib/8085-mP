from ._utils import encode,decode

class Branch:
    def __init__(self,token:dict):
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']
        
    def __jmp(self,kywrd:str):
        self.__register['SP'] = encode(decode(self.__register['SP']) - 1) 
    
    def __jc(self, kywrd:str):    
        if self.__flag['C']: self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
        
    def __jnc(self, kywrd:str):
        if not self.__flag['C']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
    
    def __jz(self, kywrd:str):
        if self.__flag['Z']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
        
    def __jnz(self, kywrd:str):
        if not self.__flag['Z']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
    
    def __jpe(self, kywrd:str):
        if self.__flag['P']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
        
    def __jpo(self, kywrd:str):
        if not self.__flag['P']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
    
    def __jm(self, kywrd:str):
        if self.__flag['S']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
        
    def __jp(self, kywrd:str):
        if not self.__flag['S']:self.__register['SP'] = encode(decode(self.__register['SP']) - 1)
    
    def get_inst(self):
        return {
            'JMP':self.__jmp,
            'JC':self.__jc,
            'JNC':self.__jnc,
            'JZ':self.__jz,
            'JNZ':self.__jnz,
            'JPE':self.__jpe,
            'JPO':self.__jpo,
            'JM':self.__jm,
            'JP':self.__jp
        }