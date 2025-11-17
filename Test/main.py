from pathlib import Path

PATH = Path(__file__).parent / 'Programs'

with open(PATH / 'test_db.asm', 'r') as file:
    program1 = file.read()

    print(program1)

from M8085 import Parser, _STACK, Assembler, Processor, Register, Memory, Flag

parser = Parser(program1)
parsed_program1 = parser.parse()

# pc = Assembler()
# pc.pass2()
# print(_STACK)

process = Processor(program1)

print(process.execute())