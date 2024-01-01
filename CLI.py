from cmd import Cmd
from os import system
from prettytable import PrettyTable
from mP import Simulator

class Interface(Cmd):
    intro = """
    Welcome to the 8085 Microprocessor Simulator!

    This simulator allows you to interact with an emulated 8085 microprocessor.
    Type 'help' for a list of available commands or 'help <command>' for detailed information.

    Get started by entering commands such as 'MOV A, B' or 'LXI H, 2000H'.
    """
    prompt = "> "
    doc_header = "Help line"
    ruler = '-'

    def __init__(self):
        super().__init__()
        self.mP = Simulator()

    def do_quit(self, arg):
        "Quits your program"
        return True
    
    def check_param(self,inst:str,arg:str):
        """
        50: syntax error -> ,
        100: invalid parameter
        200: syntax error -> param
        300: syntax error -> param:1 
        400: syntax error -> param:2
        500: register error -> param
        550: memory error -> param
        570: port error -> param
        600: register error -> param:1
        650: memory error -> param:1
        700: register error -> param:2
        750: memory error -> param:2
        """

        prompt = arg.upper().replace(' ', '').split(',')
        check_list = self.mP.param()

        if len(check_list[inst][1:]) != len(prompt): return 100
        
        else:
            if check_list[inst][0] == 1:
                
                if check_list[inst][1] != len(prompt[0]): return 200
                
                else: 
                    if len(prompt[0]) == 1 and prompt[0] not in self.mP.show_register().keys(): return 500
                    elif len(prompt[0]) == 5 and prompt[0] not in self.mP.show_memory().keys(): return 550
                    elif len(prompt[0]) == 3 and prompt[0] not in self.mP.show_port().keys(): return 570
                    else: return prompt
            
            else:
                if arg.find(',') == -1: return 50
                if  check_list[inst][1] != len(prompt[0]): return 300

                elif  check_list[inst][2] != len(prompt[1]): return 400
                
                else:
                    if len(prompt[0]) == 1 and prompt[0] not in self.mP.show_register().keys(): return 600
                    elif len(prompt[0]) == 5 and prompt[0] not in self.mP.show_memory().keys(): return 650
                    elif len(prompt[1]) == 1 and prompt[1] not in self.mP.show_register().keys(): return 700
                    elif len(prompt[1]) == 5 and prompt[1] not in self.mP.show_memory().keys(): return 750
                    else: return prompt

    def do_MOV(self, arg:str):
        """
        Args: register destination, register source

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be MOV rd, rs).
            - If 'rd' is not a register.
            - If 'rs' is not a register.

        Notes:
            The expected syntax for the MOV instruction is 'MOV rd, rs',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            > MOV A,B
        """
        status = self.check_param('MOV',arg)

        if status == 50: print("Error:',' is missing")
        elif status == 100: print("Error:invalid parameter, should be MOV rd , rs")
        elif status == 300: print("Error: rd should be a register")
        elif status == 400: print("Error: rs should be a register")
        elif status == 600: print(f"Error: {arg.replace(' ','').split(',')[0]} not a register")
        elif status == 700: print(f"Error: {arg.replace(' ','').split(',')[1]} not a register")
        else:
            rd,rs = status
            self.mP.op_code('MOV')(rd,rs)

    def do_MVI(self, arg:str):
        """
        Execute the MVI instruction to move immediate data into a register.

        Args:
            arg (str): String representing the instruction with register and 8-bit data.

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be MVI R, 8 bit data).
            - If 'R' is not a register.
            - If the content is not 8-bit.

        Notes:
            The expected syntax for the MVI instruction is 'MVI R, 8 bit data',
            where 'R' is the destination register, and '8 bit data' is the immediate data.

        Example:
            > MVI A, 42
            Moves the immediate value 42 into register A.
        """
        status = self.check_param('MVI',arg)
        if status == 50: print("Error:',' is missing")
        elif status == 100: print("Error:invalid parameter, should be MVI R , 8 bit data")
        elif status == 300: print("Error: R should be a register")
        elif status == 400: print("Error: Content should be of 8 bit (hex)")
        elif status == 600: print(f"Error: {arg.replace(' ','').split(',')[0]} not a register")
        else:
            r,data = status
            self.mP.op_code('MVI')(r,data)        

    def do_LXI(self, arg:str):
        """
        Execute the LXI instruction to load 16-bit immediate data into a register pair.

        Args:
            arg (str): String representing the instruction with register pair and 16-bit data.

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be LXI Rp, 16 bit data).
            - If 'Rp' is not a register pair.
            - If the content is not 16-bit hexadecimal.
            - If the provided memory address is restricted or not a valid memory address.

        Notes:
            The expected syntax for the LXI instruction is 'LXI Rp, 16 bit data',
            where 'Rp' is the register pair, and '16 bit data' is the immediate 16-bit hexadecimal data.

        Example:
            > LXI H, 2000H
            Loads the immediate 16-bit hexadecimal value 2000H into register pair H-L.
        """
        status = self.check_param('LXI',arg)
        if status == 50: print("Error:',' is missing")
        elif status == 100: print("Error:invalid parameter, should be LXI Rp , 16 bit data (hex)")
        elif status == 300: print("Error: Rp should be a register")
        elif status == 400: print("Error: Content should be of 16 bit (hex)")
        elif status == 600: print(f"Error: {arg.replace(' ','').split(',')[0]} not a register")
        elif status == 750: print(f"Error: {arg.replace(' ','').split(',')[1]} is a restricted memory address or not a memory address")
        else:
            rp,data = status
            self.mP.op_code('LXI')(rp,data)  

    def do_LDA(self,arg:str):
        """
        Execute the LDA instruction to load data from a memory address into the accumulator.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - If there are insufficient parameters (should be LDA 16 bit data (hex)).
            - If the provided memory address is restricted or not a valid memory address.

        Example:
            > LDA 2000H
            Loads the accumulator with the contents stored at the memory address 2000H.
        """
        status = self.check_param('LDA',arg)
        if status == 100: print("Error: invalid parmeter, should be LDA 16 bit data (hex)")
        elif status == 200 or status == 550: print(f"Error: {arg} is a restricted memory address or not a memory address")
        else:
            self.mP.op_code('LDA')(status[0])

    def do_STA(self,arg:str):
        """
        Execute the STA instruction to store the accumulator contents into a memory address.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - If there are insufficient parameters (should be STA 16 bit data (hex)).
            - If the provided memory address is restricted or not a valid memory address.

        Example:
            > STA 2000H
            Stores the contents of the accumulator into the memory address 2000H.
        """
        status = self.check_param('STA',arg)
        if status == 100: print("Error: invalid parmeter, should be LDA 16 bit data (hex)")
        elif status == 200 or status == 550: print(f"Error: {arg} is a restricted memory address or not a memory address")
        else:
            self.mP.op_code('STA')(status[0])

    def do_LDAX(self,arg:str):
        """
        Execute the LDAX instruction to load the accumulator with data from the specified register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            - If there are insufficient parameters (should be LDAX register pair (rp)).
            - If 'rp' is not a valid register pair.

        Example:
            > LDAX B
            Loads the accumulator with the contents of the memory location specified by the register pair B.
        """
        status = self.check_param('LDAX',arg)
        if status == 100: print('Error: invalid parmeter, should be LDAX register pair (rp).')
        elif status == 200 or status == 500: print(f'Error: enter a valid register')
        else:
            self.mP.op_code('LDAX')(status[0])

    def do_STAX(self,arg:str):
        """
        Execute the STAX instruction to store the accumulator contents into the memory location specified by the register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            ValueError:
                - If there are insufficient parameters (should be STAX register pair (rp)).
                - If 'rp' is not a valid register pair.

        Example:
            > STAX D
            Stores the contents of the accumulator into the memory location specified by the register pair D.
        """
        status = self.check_param('STAX',arg)
        if status == 100: print('Error: invalid parmeter, should be STAX register pair (rp).')
        elif status == 200 or status == 500: print(f'Error: enter a valid register')
        else:
            self.mP.op_code('STAX')(status[0])
    
    def do_LHLD(self,arg:str):
        status = self.check_param('LHLD',arg)
        if status == 100: print('Error: invalid parameter, should be LHLD 16 bit memory location (hex)')
        elif status == 200 or status == 500: print(f'Error: enter a valid memory location')
        else:
            self.mP.op_code('LHLD')(status[0])

    def do_SHLD(self,arg:str):
        status = self.check_param('SHLD',arg)
        if status == 100: print('Error: invalid parameter, should be SHLD 16 bit memory location (hex)')
        elif status == 200 or status == 500: print(f'Error: enter a valid memory location')
        else:
            self.mP.op_code('SHLD')(status[0])
    
    def do_IN(self,arg:str):
        status = self.check_param('IN',arg)
        if status == 100: print('Error: invalid parameter, should be IN 8 bit port location (hex)')
        elif status == 200 or status == 500: print(f'Error: enter a valid port location')
        else:
            self.mP.op_code('IN')(status[0])

    def do_OUT(self,arg:str):
        status = self.check_param('OUT',arg)
        if status == 100: print('Error: invalid parameter, should be IN 8 bit port location (hex)')
        elif status == 200 or status == 570: print(f'Error: enter a valid port location')
        else:
            self.mP.op_code('OUT')(status[0])

    def do_exmin_memory(self,arg:str):
        """
        Display memory addresses and their contents.

        Args:
            arg (str): Comma-separated list of memory addresses.

        Raises:
            KeyError: If the provided memory address is invalid.

        Example:
            > exmin_memory 2000H, 3000H
            +----------------+--------+
            | Memory Address | Content|
            +----------------+--------+
            |     2000H      |   1A   |
            |     3000H      |   FF   |
            +----------------+--------+
        """
        memory_table = PrettyTable(['Memory Address', 'Content'])
        try:
            for i in arg.split(','):
                memory_table.add_row([i.upper(),self.mP.show('M',i.upper())])

        except KeyError: print("Error: Invalid argument!")

        else: print(memory_table)

    def do_exmin_port(self,arg:str):
        """
        Display port addresses and their contents.

        Args:
            arg (str): Comma-separated list of port addresses.

        Raises:
            KeyError: If the provided port address is invalid.

        Example:
            > exmin_port 10H, 20H
            +--------------+---------+
            | Port Address | Content |
            +--------------+---------+
            |     10H      |   0A    |
            |     20H      |   FF    |
            +--------------+---------+
        """
        port_table = PrettyTable(['Port Address', 'Content'])
        try:
            for i in arg.split(','):
                port_table.add_row([i.upper(),self.mP.show('P',i.upper())])

        except KeyError: print("Error: Invalid argument!")

        else: print(port_table)

    def do_exmin_memol(self,arg):
        """
        Display memory and its contents.

        Args: None

        Example:
            > exmin_memol
            +----------------+--------+
            | Memory Address | Content|
            +----------------+--------+
            | 8000H          | 1A     |
            | 8001H          | 2B     |
            | ...            | ...    |
            +----------------+--------+
        """
        memory_table = PrettyTable(['Memory Address', 'Content'])   
        for i in self.mP.show_memory():
            memory_table.add_row([i,self.mP.show('M',i)])
        
        print(memory_table)
    
    def do_exmin_register(self,arg):
        """
        Display registers and their contents.

        Args: None

        Example:
            > exmin_register
            +-----------+--------+
            | Register  | Content|
            +-----------+--------+
            | A         | 1A     |
            | B         | 2B     |
            | ...       | ...    |
            +-----------+--------+
        """
        register_table = PrettyTable(['Register', 'Content'])
        for i in self.mP.show_register():
            if i != 'M' and i != 'F':
                register_table.add_row([i,self.mP.show('R',i)])
        
        print(register_table)
    
    def do_exmin_flag(self,arg):
        """
        Display flags and their contents.

        Args:
            arg (str): Not used.

        Example:
            > exmin_flag
            +---+---+----+---+---+
            | S | Z | AC | P | C |
            +---+---+----+---+---+
            | 0 | 0 | 0  | 0 | 0 |
            +---+---+----+---+---+
        """
        flag_table = PrettyTable([i for i in self.mP.show_flag()])
        flag_table.add_row([self.mP.show('F',i) for i in self.mP.show_flag()])
        
        print(flag_table)
    
    def do_clear(self,arg):
        """
        Clear the console screen.

        Args:None

        Example:
            > clear
            Console screen cleared.
        """
        system('CLS')

    do_cls = do_clear

if __name__ == "__main__":
    run = Interface()
    run.cmdloop()