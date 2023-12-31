from cmd import Cmd
from os import system
from prettytable import PrettyTable
from mP import Simulator

class Interface(Cmd):
    prompt = "> "
    doc_header = "Help line"
    ruler = '-'

    def __init__(self):
        super().__init__()
        self.mP = Simulator()

    def do_quit(self, arg):
        "Quits your program"
        return True

    def do_MOV(self, arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MOV instruction is 'MOV rd, rs',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MOV A , B
        """
        if len(arg) > 5:
            print("Error: Should be MOV rd , rs")
        
        elif arg.find(',') == 1:
            arg.upper()
            rd,rs = arg.upper().split(',')
            self.mP.op_code('MOV')(rd,rs)

        else:
            print("Error: your forgot ',' should be MOV rd , rs ")

    def do_MVI(self, arg:str):
        """
        Args:
            arg (str): register, data

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'r' is the register and 'data' is content to be stored.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 5:
            print("Error: Should be MIV r , data")
        
        elif arg.find(',') == 1:
            r,data = arg.upper().split(',')
            self.mP.op_code('MVI')(r,data)

        else:
            print("Error: your forgot ',' should be MIV r , data")

    def do_LXI(self, arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 7:
            print("Error: Should be LXI rp , data (16-bit)")
        
        elif arg.find(',') == 1:
            rp,data = arg.upper().split(',')
            self.mP.op_code('LXI')(rp,data)

        else:
            print("Error: your forgot ',' should be LXI rp , data (16-bit)")
    
    def do_LDA(self,arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 5:
            print("Error: should be LDA memory(16-bit)")
        
        elif arg.find(',') == -1:
            self.mP.op_code('LDA')(arg.upper())

        else:
            print("Error: should be LDA memory(16-bit)")
    
    def do_LDAX(self,arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 2 or len(arg) < 2:
            print("Error: should be LDAX rp(register pair)")
        
        elif arg.find(',') == -1:
            self.mP.op_code('LDAX')(arg.upper())

    def do_STAX(self,arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 2:
            print("Error: should be STAX rp(register pair)")
        
        elif arg.find(',') == -1:
            if arg != 'H':
                self.mP.op_code('STAX')(arg.upper())
            else:
                print("Error: STAX H instruction does not exists!")
    
    def do_STA(self,arg:str):
        """
        Args:
            arg (str): register destination, register source

        Raises:
            ValueError: If the syntax is incorrect or if the ',' is missing.

        Notes:
            The expected syntax for the MIV instruction is 'MIV r, data',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            >>> MIV A , 95H
        """
        if len(arg) > 5:
            print("Error: should be LDA memory(16-bit)")
        
        elif arg.find(',') == -1:
            self.mP.op_code('STA')(arg.upper())

        else:
            print("Error: should be LDA memory(16-bit)")

    def do_exmin_memory(self,arg:str):
        'Display\'s memory and its contents'
        memory_table = PrettyTable(['Memory Address', 'Content'])
        try: memory_table.add_row([arg.upper(),self.mP.show('M',arg.upper())])

        except KeyError: print("Error: Invalid input!")

        else: print(memory_table)

    def do_exmin_memol(self,arg):
        'Display\'s memory and its contents'
        memory_table = PrettyTable(['Memory Address', 'Content'])
        for i in self.mP.show_memory():
            memory_table.add_row([i,self.mP.show('M',i)])
        
        print(memory_table)
    
    def do_exmin_register(self,arg):
        'Display\'s register and its contents'
        register_table = PrettyTable(['Register', 'Content'])
        for i in self.mP.show_register():
            if i != 'M' and i != 'F':
                register_table.add_row([i,self.mP.show('R',i)])
        
        print(register_table)
    
    def do_exmin_flag(self,arg):
        'Display\'s flag and its contents'
        flag_table = PrettyTable(['Flag', 'Value'])
        for i in self.mP.show_flag():
            flag_table.add_row([i,self.mP.show('F',i)])
        
        print(flag_table)
    
    def do_clear(self,arg):
        system('CLS')

    do_cls = do_clear

run = Interface()
run.cmdloop()