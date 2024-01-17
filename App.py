import streamlit as st
from prettytable import PrettyTable
from mP import Simulator

st.set_page_config(page_title="8085 Simulator",page_icon="icon.png")
st.title('Welcome to 8085 Simulator')
st.markdown("""
This simulator allows you to interact with an emulated 8085 microprocessor.
Type 'help' for a list of available commands or 'help <command>' for detailed information.

Get started by entering commands such as 'MOV A, B' or 'LXI H, 2000H'.

__- By Sakar Giri (KAN079BEI016)__""")

class App(Simulator):
    def __init__(self):
        super().__init__()
        self.error_msg = {
            'CommaError':lambda:[st.chat_message("assistant").write('Error: , missing'),
                self.history('assistant','Error: , missing')],
            'SyntaxError': lambda arg,syntax: [st.chat_message("assistant").write(f'Invalid Syntax: {arg}. Should be {syntax}.'),
                self.history('assistant',f'Invalid Syntax: {arg}. Should be {syntax}.')],
            'TypeError':lambda:[st.chat_message("assistant").write('TypeError: Argument(s) missing'),
                self.history('assistant','TypeError: Argument(s) missing')],
            'RpError': lambda arg:[st.chat_message("assistant").write(f'RpError: {arg}. Should be a vaild register pair (i.e B,C,D,E,H,L).'),
                self.history('assistant',f'RpError: {arg}. Should be a vaild register pair (i.e B,C,D,E,H,L).')],
            'NoArgumentError':lambda inst:[st.chat_message("assistant").write(f'{inst} takes no argument.'),
                self.history('assistant',f'{inst} takes no argument.')],
            'PointerError':lambda pointer:[st.chat_message("assistant").write(f'PointerError: {pointer} is not pointing to any memory address.'),
                self.history('assistant',f'PointerError: {pointer} is not pointing to any memory address.')],
            'RegisterError':lambda register:[st.chat_message("assistant").write(f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)'),
                self.history('assistant',f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)')],
            'DataError':lambda data:[st.chat_message("assistant").write(f'DataError: {data} should be a valid 8-bit data.'),
                self.history('assistant',f'DataError: {data} should be a valid 8-bit data.')],
            'MemoryError':lambda memory:[st.chat_message("assistant").write(f'MemoryError: {memory} should be a valid 16-bit memory address.'),
                self.history('assistant',f'MemoryError: {memory} should be a valid 16-bit memory address.')],
            'PortError':lambda port:[st.chat_message("assistant").write(f'PortError: {port} should be a vaild 8-bit port address.'),
                self.history('assistant',f'PortError: {port} should be a vaild 8-bit port address.')]
        }
        self.specify_msg = {
            'MOV':{
                'SyntaxError':'MOV rd,rs',
            },
            'MVI':{
                'SyntaxError':'MVI r,data (8-bit)',
            },
            'LXI':{
                'SyntaxError':'LXI rp,memory address',
            },
            'LDA':{
                'SyntaxError':'LDA 16-bit memory address',
            },
            'STA':{
                'SyntaxError':'STA 16-bit memory address',
            },
            'LDAX':{
                'SyntaxError':'LDAX register pair (rp)',
            },
            'STAX':{
                'SyntaxError':'STAX register pair (rp)',
            },
            'LHLD':{
                'SyntaxError':'LHLD 16 bit memory location (hex)'
            },
            'SHLD':{
                'SyntaxError':'SHLD 16 bit memory location (hex)'
            },
            'IN':{
                'SyntaxError':'IN 8 bit port location',
            },
            'OUT':{
                'SyntaxError':'OUT 8 bit port location',
            },
            'XCHG':{
                'SyntaxError':'XCHG takes no argument',
            },
            'ADD':{
                'SyntaxError':'ADD r/m',
            },
            'ADC':{
                'SyntaxError':'ADC r'
            },
            'ADI':{
                'SyntaxError':'ADI 8-bit data'
            },
            'DAD':{
                'SyntaxError':'DAD Rp'
            },
            'SUB':{
                'SyntaxError':'SUB r/m'
            },
            'SUI':{
                'SyntaxError':'SUI 8-bit data (hex)'
            },
            'SBI':{
                'SyntaxError':'SBI 8-bit data (hex)'
            },
            'SBB':{
                'SyntaxError':'SBB r/m'
            },
            'INR':{
                'SyntaxError':'INR r/m'
            },
            'DCR':{
                'SyntaxError':'DCR r/m'
            },
            'INX':{
                'SyntaxError':'INX Rp'
            },
            'DCX':{
                'SyntaxError':'DCX Rp'
            }
        }
        if "register" not in st.session_state:
            st.session_state.register = self.show_register()
        if "memory" not in st.session_state:
            st.session_state.memory = self.show_memory()
        if "flag" not in st.session_state:
            st.session_state.flag = self.show_flag()

        self.display()

    def display(self):

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input("Command here . . ."):
            st.chat_message("user").write(prompt)
            self.history("user",prompt)
            self.scrap(prompt)

    def history(self,role:str,content:str):
        st.session_state["messages"].append({"role":role,"content":content})

    def scrap(self,prompt:str):
        prompt_chunk = prompt.split(" ")
        if prompt_chunk[0] in self.show_op_code():
            inst,param = prompt_chunk[0], ''.join(prompt_chunk[1:])
            status = self.check_param(inst,param)
            if status == 'CommaError' or status == 'TypeError':self.error_msg[status]()
            elif status == 'SyntaxError':self.error_msg[status](prompt,self.specify_msg[inst][status])
            elif status == 'MemoryError':self.error_msg[status](prompt)
            elif status == 'RegisterError':self.error_msg[status](prompt)
            elif status == 'PortError':self.error_msg[status](prompt)
            elif status == 'DataError':self.error_msg[status](prompt)
            elif status == 'PointerError':self.error_msg[status]('M')
            elif inst in ['LDAX','STAX'] and self.check_pointer(param[0]): self.error_msg['PointerError'](param[0])
            elif inst in ['LXI','LDAX','STAX'] and ( status == 'RegisterError' or param[0] in ['A','M','F']):
                self.error_msg['RpError'](param[0])
            else:
                if inst in ['MOV','MVI','LXI']:
                    self.op_code(inst)(status[0],status[1])
                elif inst in ['XCHG']:
                    self.op_code(inst)()
                else:
                    self.op_code(inst)(status[0])
                
                st.session_state.register = self.show_register()
                st.session_state.memory = self.show_memory()
                st.session_state.flag = self.show_flag()

        elif prompt_chunk[0] == 'exam:memory':
            memory_list = ''.join(prompt_chunk[1:])
            memory_table = PrettyTable(['Memory Address', 'Content'])
            try:
                for i in memory_list.split(','):
                    memory_table.add_row([i.upper(),st.session_state["memory"][i.upper()]])

            except KeyError:
                st.chat_message('assistant').write('Error: TypeError: Parameter not fulfilled.')
                self.history('assistant','TypeError: Parameter not fulfilled.')

            else:
                st.chat_message('assistant').write(memory_table)
                self.history('assistant',memory_table)

        elif prompt_chunk[0] == 'exam:register':
            register_table = PrettyTable(['Register', 'Content'])
            for i in self.show_register():
                if i != 'M' and i != 'F':
                    register_table.add_row([i,st.session_state["register"][i]])
            st.chat_message('assistant').write(register_table)
            self.history('assistant',register_table)

        else:
            st.chat_message("assistant").write(f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
            self.history("assistant",f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
            
if __name__ == "__main__":
    app = App()