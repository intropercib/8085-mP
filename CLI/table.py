from pathlib import Path

from rich.table import Table as RichTable
from rich.console import Console
import yaml


class Table(RichTable):
    def __init__(self, header:list | range, row: list):
        super().__init__()
        
        path = Path(__file__).parent / "table_commands.yaml"
        # with open(path, 'r') as file:
        #     self.command_docs = yaml.safe_load(file)
        
        self.row = map(lambda x: str(x) if isinstance(x,int) else x, row)
        self.header = map(lambda x: str(x) if isinstance(x,int) else x, header)

    def _generate_table(self):
        
        for c in self.header:
            self.add_column(c, justify="center", style="blue", no_wrap=True)

        for r in self.row:
            self.add_row(*r)

        return self

        
register = {
    'A':'00H','B':'90H','C':'00H','D':'00H','E':'00H','H':'00H','L':'00H','M':'00H',
    'PC':'0000H','SP':'0000H'
}
# flag = {'S':0,'Z':0,'AC':0,'P':0,'C':0}

memory =  [ [hex(i), '00H'] for i in range(11) ]

# print(memory)
console = Console()
table = Table(register.keys(), register.values())
console.print(table._generate_table())