from cmd import Cmd
import os
import time
from pathlib import Path

from Backend.M8085 import Register, Memory, Flag, Processor, Assembler

from .decorators import process_memory, groq_request
from .theme import console, STYLE, intro_panel, create_table

class Interface(Cmd):
    prompt = "> "
    doc_header = "Available Commands"
    ruler = '═'

    def __init__(self):
        super().__init__()
        self.do_clear(0)

        path = Path()
        self.loc = path.home() / "Documents" / "8085_Programs"
        self.loc.mkdir(parents=True, exist_ok=True)


        self.code = ""
        self.register = Register()
        self.memory = Memory()
        self.flag = Flag()

    def preloop(self):
        console.print(intro_panel())

    def response(self, string: str, style: str = "text", delay: float = 0.008):
        styled = f"[{style}]{string}[/{style}]"
        if delay > 0:
            for char in string:
                console.print(char, end='', style=style)
                time.sleep(delay)
            console.print()
        else:
            console.print(styled)
    
    def do_clear(self, arg):
        """Clear the terminal screen.
        
        Usage:
            clear
        
        Example:
            > clear
        """
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

    def default(self, line):
        self.code += line + "\n"
    
    def do_run(self, arg:str):
        """Execute 8085 assembly code from buffer or load and run from a file.
        
        Usage:
            run [filename.asm]
        
        Examples:
            > MVI A, 05H
            > INR A
            > HLT ; Note: hlt should be the last instruction or else code will not execute.
            > run              # Executes the code in buffer
            
            > run program1.asm # Loads and executes program1.asm
        
        Notes:
            - If no filename is provided, executes code in the current buffer
            - If filename is provided, loads code from home/Documents/8085_Programs/
            - Buffer is cleared after execution
        """
        if arg.endswith('.asm'):
            file_path = self.loc / arg
            if not file_path.exists():
                self.response(f"File {arg} not found in {self.loc}", style="error")
                return
            with open(file_path, 'r') as f:
                self.code = f.read()
            
            self.response(f"Loaded code from {file_path}", style="success")

        console.print("[subheader]=== Executing Code ===[/]")
        for i, line in enumerate(self.code.splitlines(), start=1):
            console.print(f"[muted]{i:3}[/] [instruction]{line}[/]")

        console.print()

        processor = Processor(self.code)
        result = processor.execute()
        if result:
            self.response(result, style="success")
        
        self.code = ""
    
    def do_showprograms(self, arg):
        """Display all available .asm program files in the programs directory.
        
        Usage:
            showprograms
        
        Example:
            > showprograms
        
        Notes:
            - Shows files from home/Documents/8085_Programs/
            - Displays filename and full path in a table
        """
        files = list(self.loc.glob("*.asm"))
        if not files:
            self.response("No .asm files found in the programs directory.", style="error")
            return
        
        table = create_table("Filename", title="8085 Programs\n(Location: home/Documents/8085_Programs/)")
        for file in files:
            table.add_row(f"[filename]{file.name}[/]")
        
        console.print(table)
        console.print()

    def do_register(self, arg):
        """Display the current state of all 8085 processor registers.
        
        Usage:
            register
        
        Example:
            > register
        
        Notes:
            - Shows all general purpose registers (A, B, C, D, E, H, L)
            - Shows register pairs (BC, DE, HL)
            - Shows program counter (PC) and stack pointer (SP)
        """
        table = create_table(*self.register.get_all().keys(), title="REGISTERS")
        registers = self.register.get_all()
        table.add_row(*[f"[value]{v}[/]" for v in registers.values()])
        console.print(table)
        console.print()

    @process_memory
    def do_memory(self, arg):
        """Display memory contents at specified addresses.
        
        Usage:
            memory <address_start> - <address_end>
            memory <address1>, <address2>, <address3>...
            memory <address>
        
        Examples:
            > memory 0001H - 00FFH # Shows values from address 0001H to 00FFH
            > memory 2000H, 2001H # Shows values at addresses 2000H and 2001H
            > memory 0000H       # Shows value at address 0000H
        
        Notes:
            - Addresses should be in hexadecimal format (e.g., ABCDH)
            - Multiple addresses can be specified separated by commas
            - Address ranges can be specified using a hyphen
            - Displays address and corresponding value in a table
        """
        table = create_table("Address", "Value", title="MEMORY")

        for address in arg:
            value = self.memory[address]
            table.add_row(f"[address]{address}[/]", f"[value]{value}[/]")
        
        console.print(table)
        console.print()

    def do_flag(self, arg):
        """Display the current state of all processor flags.
        
        Usage:
            flag
        
        Example:
            > flag
        
        Notes:
            - Shows all 5 flags: Sign (S), Zero (Z), Auxiliary Carry (AC), Parity (P), Carry (C)
            - Flag values are shown as 0 or 1
        """
        table = create_table(*self.flag.get_all().keys(), title="FLAGS")
        flags = self.flag.get_all()
        table.add_row(*[f"[value]{v}[/]" for v in flags.values()])
        console.print(table)
        console.print()
    
    def do_assemble(self, arg):
        """Assemble the current code buffer and display the assembled output.
        
        Usage:
            assemble
        
        Example:
            > MVI A, 05H
            > INR A
            > HLT
            > assemble
        
        Notes:
            - Performs two-pass assembly on the current code buffer
            - Displays address, label, instruction, opcode, cycles, and operand
            - Does not execute the code (use 'run' for execution)
        """
        assembler = Assembler()
        assembler.pass2()
        assembled = assembler.assemble()

        table = create_table('Address', 'Label', 'Instruction', 'Opcode', 'Cycles', 'Operand', title="ASSEMBLED TABLE")
        
        for row in assembled:
            styled_row = [
                f"[address]{row[0]}[/]",
                f"[label]{row[1]}[/]",
                f"[instruction]{row[2]}[/]",
                f"[opcode]{row[3]}[/]",
                f"[muted]{row[4]}[/]",
                f"[value]{row[5]}[/]",
            ]
            table.add_row(*styled_row)

        console.print(table)
        console.print()
    
    def do_timing(self, arg):
        arg = arg.strip().upper()
        """Display the timing diagram for a specified 8085 instruction.
        
        Usage:
            timing <instruction>
        
        Example:
            > timing MOV
        Notes:
            - Instruction should be a valid 8085 mnemonic (e.g., MOV, MVI, ADD)
            - Displays the timing diagram as ASCII art in the terminal
        """
        import webbrowser
        from Backend.M8085._timing import TimingDiagram

        td = TimingDiagram()
        fig = td.as_dict(arg)
        if fig:
            # Create data URL and open in browser
            webbrowser.open(fig['diagram'])
            self.response(f"Timing diagram for instruction '{arg}' opened in web browser.", style="success")    
            
        else:
            self.response(f"Error: No instruction named {arg}", style="error")

    
    def do_setkey(self, arg):
        """Store your Groq API key securely in the system keyring.
        
        Usage:
            setkey <your_groq_api_key>
        
        Example:
            > setkey gsk_1234567890abcdef
        
        Notes:
            - API key is required to use the 'ask' command
            - Key is stored securely using the system's keyring service
            - Use 'deletekey' to remove the stored key
        """
        import keyring

        service_name = "8085mp"
        key_name = "groq_api_key"

        if not arg.strip():
            self.response("Usage: setkey <your_groq_api_key>", style="error")
            return

        keyring.set_password(service_name, key_name, arg.strip())
        self.response("API key set successfully.", style="success")
    
    def do_deletekey(self, arg):
        """Delete the stored Groq API key from the system keyring.
        
        Usage:
            deletekey
        
        Example:
            > deletekey
        
        Notes:
            - Removes the API key stored by 'setkey' command
            - You'll need to use 'setkey' again to use the 'ask' command
        """
        import keyring

        service_name = "8085mp"
        key_name = "groq_api_key"

        keyring.delete_password(service_name, key_name)
        self.response("API key deleted successfully.", style="success")

    @groq_request(2005)
    def do_ask(self, prompt):
        """Ask a question to the AI assistant about 8085 microprocessor.
        
        Usage:
            ask <your question>
        
        Examples:
            > ask How does the MOV instruction work?
            > ask Explain the difference between CALL and PUSH
            > ask Write a program to add two numbers
        
        Notes:
            - Requires API key to be set using 'setkey' command
            - Response is rendered as formatted Markdown
            - Useful for getting help with 8085 programming concepts
        """
        from rich.markdown import Markdown
        console.print(Markdown(prompt))

    def do_clear_code(self, arg):
        """Clear the current code buffer without executing.
        
        Usage:
            clear_code
        
        Example:
            > MVI A, 05H
            > INR A
            > clear_code      # Clears the buffer
        
        Notes:
            - Removes all code from the buffer
            - Use this when you want to start fresh without running current code
        """
        self.code = ""
        self.response("Code buffer cleared.", style="success", delay=0)

    def do_exit(self, arg):
        """Exit the 8085 simulator.
        
        Usage:
            exit
        
        Example:
            > exit
        
        Notes:
            - Closes the simulator and returns to the shell
            - Any code in the buffer will be lost
        """
        console.print("[muted]Goodbye.[/]")
        return True  
    
    def do_help(self, arg):
        if arg:
            try:
                func = getattr(self, 'do_' + arg)
                console.print(func.__doc__ or "No detailed help available for this command.",style="accent")
            except AttributeError:
                self.response(f"No such command: {arg}", style="error")
        else:
            cmds = [cmd_name[3:] for cmd_name in self.get_names() if cmd_name.startswith('do_')]
            console.print("[label]Available Commands:[/]")
            table = create_table("Command", title="COMMANDS")
            for _ in cmds:
                table.add_row(_,style="instruction")
            console.print(table)

            console.print("\nType [accent]help <command>[/accent] for detailed help on a specific command.\n")
    

    def do_docs(self, arg):
        """Display documentation from a YAML file.
        
        Usage:
            docs <path_to_yaml_file>
        
        Example:
            > docs docs/commands.yaml"""
        if arg:
            arg = arg.upper()
            from yaml import safe_load
            
            path = Path(__file__).parent.parent / "Backend" / "M8085" / "docs.yml"

            with open(path, "r") as f:
                docs = safe_load(f)
                console.print(docs.get(arg, "No documentation found for this topic."))

        else:
            self.response("Usage: docs <name of instruction>", style="error")

if __name__ == "__main__":
    interface = Interface()
    interface.cmdloop()