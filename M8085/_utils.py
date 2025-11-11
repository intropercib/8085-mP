from pathlib import Path
import yaml

PATH = Path(__file__).parent

with open(f"{PATH}/commands_property.yml", "r") as f:
    INSTRUCTION:dict = yaml.safe_load(f)

def decode(arg:str) -> int:
    arg = arg[:-1]  # Remove 'H' at the end
    try:
        return int(arg,16)
    except ValueError:
        return f'Invalid Address: {arg}'

def encode(arg:int, bit:int=2) -> str:

    addr = hex(arg)[2:].upper()

    if len(addr) < bit:
        return '0' * (bit - len(addr)) + addr + 'H'
    
    return addr + 'H'
