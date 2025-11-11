from cmd import Cmd
import time
import os


class Interface(Cmd):
    intro = """
    Welcome to the 8085 Microprocessor Simulator!

    This simulator allows you to interact with an emulated 8085 microprocessor.
    Type 'help' for a list of available commands or 'help <command>' for detailed information.

    Get started by entering commands such as 'MOV A, B' or 'LXI H, 8000H'.
    """
    prompt = "> "
    doc_header = "Avaliable Help"
    ruler = '-'

    def __init__(self):
        super().__init__()
        if os.name == 'nt': os.system('cls')
        elif os.name == 'posix': os.system('clear')

        self.session = {"messages":[]}

    def default(self,prompt):
        self.response(prompt)

    def do_quit(self, arg):
        "Quits your program"
        return True
        
    # def do_assemble(self,arg):
    #     print(self.cu.assemble())

    def response(self,string:str, delay=0.018):
        for char in string:
            print(char, end ='', flush=True)
            time.sleep(delay)
        print('\n')

    def history(self, role:str, content:str):
        self.session["messages"].append({"role":role,"content":content})
    
    def do_help(self, arg: str):
        remove_space = ''.join(arg.split(' '))
        for i in remove_space.split(','):
            try:
                self.response("="*100 + f"\n{i}:\n" + "="*100,0.003)
                self.response(Interface.command_docs[i],0.003)
                self.response("="*100,0.003)
            except KeyError:
                self.response(f"Unknown command: {arg}.Type 'help <command name>' for a list of commands.")

    def do_clear(self,arg):
        """
        Clear the console screen.

        Args:None

        Example:
            > clear
            Console screen cleared.
        """
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

    do_cls = do_clear

if __name__ == "__main__":
    run = Interface()
    run.cmdloop()