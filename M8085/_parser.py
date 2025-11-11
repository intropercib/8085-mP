from pyparsing import (
Combine, Word, Literal, Optional, Group, Suppress, MatchFirst, 
Keyword, Regex, ParseException, ZeroOrMore, LineEnd, StringEnd,
alphas, alphanums, restOfLine, lineno, col, line,
)

from ._utils import decode, INSTRUCTION

IDENTIFIER = Word(alphas + "_", alphanums + "_")  # label
HEX_ADDRESS = Regex(r'[0-9A-F]+H') # e.g. 2000H
REGISTER = Word("ABCDEHLM", exact=1) | Literal("SP") | Literal("PSW") | Literal('PC')
MNEMONICS =  MatchFirst(
map(lambda m:Keyword(m), INSTRUCTION.keys())
) ('inst')
MEMORY_RANGE:range = range(65536)
PORT_RANGE:range = range(256)

class Message:
    def __init__(
        self, msg:str, inst:str, pos:str, line:str, tag:str = None, format:str = None
        ) -> str:        
        self.msg = msg
        self.inst = inst
        self.pos = pos
        self.line = line
        self.format = format
        self.tag = tag
        self.general = f'{self.msg} for {self.inst} at {self.pos} -> {self.line}'

    def __tag_map(self) -> str:

        msg = {
        'm:8': '8-bit Memory Address is reserved or out of range',
        'm:16': '16-bit Memory Address is reserved or out of range',
        'r': 'Invalid Register Used',
        'rp': 'Invalid Register Pair Used',
        'l': 'Undefined Label Reference'
        }

        self.general = f'{msg.get(self.tag)}. at {self.pos} -> {self.line}'

    def __str__(self) -> str:
        if self.tag:
            self.__tag_map()

        if self.format:
            self.general += f'\nHint: {self.format}'

        return self.general

class Parser:

    def __init__(self,code:str):
        # Label definition: LABEL:
        label = Group(IDENTIFIER + Suppress(":")) ('label')
        #operands
        operand = IDENTIFIER | HEX_ADDRESS
        #instruction
        instruction = (
        MNEMONICS + Optional(operand('op1') + Optional(Suppress(",") + operand('op2')))
        )('code')
        # Comment: ; rest of line
        comment = Group(Suppress(";") + restOfLine) ('comment')

        self._rules = (
            label + instruction + comment |
            label + instruction |
            label + comment |
            instruction + comment |
            label |
            instruction |
            comment
        )

        self._code = code.upper()
        self._label = 'START'
        self._structure = {'START':[]}
        self._operand = {
        'm:8': self.__check_addr8,
        'm:16': self.__check_addr16,
        'r': self.__check_register,
        'l': self.__check_reference,
        'rp': self.__check_rp
        }

    def __preprocess(self):
        return filter(lambda line: line.strip() != '', self._code.splitlines())

    def __add_line_info(self,parsed:dict, line:str, idx:int):
        parsed['pos'] = f"line: {idx} col: 1"
        parsed['line'] = line.strip()
        return parsed

    @property
    def structure(self):
        for idx, line in enumerate(self.__preprocess(), start=1):
            try:
                parsed = self._rules.parseString(line)
                wrapped = self.__add_line_info(parsed.asDict(), line, idx)
                result = self._param_check(wrapped)
                if isinstance(result,Message):
                    return result
            except ParseException as p:
                key = p.found[1:-1] # p.found is in quotes by default. Removed them.
                if key in map(lambda m:m, INSTRUCTION.keys()):
                    expected = INSTRUCTION[key]['syntax']
                    return Message('Invalid Syntax',key,f'line: {idx}, col: {p.col}',p.line,format=expected)
                else:
                    return Message('Invalid Syntax',p.found,f'line: {idx}, col: {p.col}',p.line)

        return self._structure


    def _param_check(self,line:dict[str:str]):
        if 'label' in line:
            self._label = line['label'][0]
            self._structure[ self._label ] = []

        if 'inst' in line:

            inst = line['inst']
            code = line['code']
            param_rule = INSTRUCTION[inst]['param_rule']

            if param_rule:
                if len(code[1:]) != len(param_rule):
                    return Message('Invalid Operand',inst,line['pos'],line['line'],
                        format=INSTRUCTION[inst]['syntax']
                    )

                for i in range(len(param_rule)):
                    operand = code[i+1]
                    rule = param_rule[i]
                    result = self._operand.get( rule )( operand )

                if not result:
                    syntax = INSTRUCTION[inst]['syntax']
                    return Message('Invalid',inst,line['pos'],line['line'],tag=rule,format=syntax)

            if self._label in self._structure:
                self._structure.get(self._label).append(code)


    def __check_addr8(self,operand:str): return decode(operand) in PORT_RANGE

    def __check_addr16(self,operand:str): return decode(operand) in MEMORY_RANGE

    def __check_register(self,operand:str): 
        try:
            REGISTER.parseString(operand,parseAll=True)
            return True
        except ParseException: return False

    def __check_reference(self,operand:str): return self._code.find(operand) != -1

    def __check_rp(self,operand:str): return operand in ['B','D','H']