from pathlib import Path
import yaml
from .logs import setup_logger, warn
setup_logger()

PATH = Path(__file__).parent

with open(f"{PATH}/commands_property.yml", "r") as f:
    INSTRUCTION:dict = yaml.safe_load(f)

def decode(arg:str) -> int | str:
    arg = arg[:-1]  # Remove 'H' at the end
    try:
        return int(arg,16)
    except ValueError:
        warn(f"Invalid Address: {arg}")
        return f"Invalid Address: {arg}"

def encode(arg:int, bit:int=2) -> str:

    addr = hex(arg)[2:].upper()

    if len(addr) < bit:
        return '0' * (bit - len(addr)) + addr + 'H'
    
    return addr + 'H'

def operate(op1: str | int, op2: str | int, flag: int = 0, bit: int = 2) -> str:
    if isinstance(op1, str):
        op1 = decode(op1)
    
    if isinstance(op2, str):
        op2 = decode(op2)

    return encode(op1 + op2 + flag, bit=bit)