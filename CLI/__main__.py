from cmd import Cmd
import os
import time
from pathlib import Path

from Backend.M8085 import Register, Memory, Flag, Processor, Assembler

from .decorators import process_memory
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
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

    def default(self, line):
        self.code += line + "\n"
    
    def do_run(self, arg:str):

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
    
    def do_show_programs(self, arg):
        files = list(self.loc.glob("*.asm"))
        if not files:
            self.response("No .asm files found in the programs directory.", style="error")
            return
        
        table = create_table("Filename", "Path", title="8085 Programs")
        for file in files:
            table.add_row(f"[filename]{file.name}[/]", f"[path]{file}[/]")
        
        console.print(table)
        console.print()

    def do_register(self, arg):
        table = create_table(*self.register.get_all().keys(), title="REGISTERS")
        registers = self.register.get_all()
        table.add_row(*[f"[value]{v}[/]" for v in registers.values()])
        console.print(table)
        console.print()

    @process_memory
    def do_memory(self, arg):
        table = create_table("Address", "Value", title="MEMORY")

        for address in arg:
            value = self.memory[address]
            table.add_row(f"[address]{address}[/]", f"[value]{value}[/]")
        
        console.print(table)
        console.print()

    def do_flag(self, arg):
        table = create_table(*self.flag.get_all().keys(), title="FLAGS")
        flags = self.flag.get_all()
        table.add_row(*[f"[value]{v}[/]" for v in flags.values()])
        console.print(table)
        console.print()
    
    def do_assemble(self, arg):
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

    def do_clear_code(self, arg):
        self.code = ""
        self.response("Code buffer cleared.", style="success", delay=0)

    def do_exit(self, arg):
        """Exit the simulator."""
        console.print("[muted]Goodbye.[/]")
        return True  

    def request_api_key(self) -> bool:
        """Prompt the user for an OpenAI API key and store it in the environment.

        Returns True if a key was provided and stored, False otherwise.
        """
        try:
            self.response("OpenAI API key is required to run the assistant.\nYou can paste it now (it will be stored only in this session):", style="muted", delay=0)
            key = input("OpenAI API key (or blank to cancel): ").strip()
            if not key:
                self.response("API key not provided.", style="error", delay=0)
                return False
            os.environ["OPENAI_API_KEY"] = key
            self.response("API key saved to environment for this session.", style="success", delay=0)
            return True
        except Exception:
            return False

if __name__ == "__main__":
    interface = Interface()
    interface.cmdloop()