from rich.table import Table
from rich.console import Console
import random


def main():
    console = Console()
    console.print("[bold green]Welcome to M8085 Emulator[/bold green]\n")
    
    # Create table with random data
    table_obj = Table(title="[bold cyan]8085 CPU Registers[/bold cyan]", show_header=True, header_style="bold magenta")
    table_obj.add_column("Register", justify="center", style="cyan", no_wrap=True)
    table_obj.add_column("Hex Value", justify="center", style="green")
    table_obj.add_column("Decimal", justify="center", style="yellow")
    table_obj.add_column("Binary", justify="center", style="blue")
    
    # Add random data for 8085 registers
    registers = ["A", "B", "C", "D", "E", "H", "L", "PC", "SP"]
    for reg in registers:
        value = random.randint(0, 255)
        table_obj.add_row(
            reg,
            f"{value:02X}h",
            str(value),
            f"{value:08b}b"
        )
    
    console.print(table_obj)


if __name__ == "__main__":
    main()