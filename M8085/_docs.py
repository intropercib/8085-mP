class Docs:
    command_docs = {
    "MOV": """
        Move data from one register to another.

        Args:
            arg (str): The arguments should be in the format 'MOV rd, rs', where 'rd' is the destination register and 'rs' is the source register.

        Raises:
            - CommaError: If the ',' is missing.
            - SyntaxError: If the syntax is incorrect.
            - RpError: If the provided register pair is not valid (i.e., B, C, D, E, H, L).
            - RegisterError: If the provided register is not valid.
            - NoArgumentError: If the instruction takes no argument.
        
        Notes:
            The MOV instruction copies the contents of the source register 'rs' to the destination register 'rd'.

        Example:
            > MOV A, B
            Moves the content of register B to register A.
    """,
    "MVI": """
        Move immediate data into a register.

        Args:
            arg (str): String representing the instruction with register and 8-bit data.

        Raises:
            - CommaError: If the ',' is missing.
            - SyntaxError: If the syntax is incorrect.
            - RpError: If the provided register pair is not valid (i.e., B, C, D, E, H, L).
            - RegisterError: If the provided register is not valid.
            - DataError: If the provided data is not valid (not 8-bit).
        
        Notes:
            The MVI instruction moves immediate 8-bit data into the specified register.

        Example:
            > MVI A, 42
            Moves the immediate value 42 into register A.
    """,
    "LXI": """
        Load 16-bit immediate data into a register pair.

        Args:
            arg (str): String representing the instruction with register pair and 16-bit data.

        Raises:
            - CommaError: If the ',' is missing.
            - SyntaxError: If the syntax is incorrect.
            - RpError: If the provided register pair is not valid (i.e., B, D, H).
            - MemoryError: If the provided memory address is not valid.
        
        Notes:
            The LXI instruction loads 16-bit immediate data into the specified register pair.

        Example:
            > LXI H, 2000H
            Loads the immediate 16-bit hexadecimal value 2000H into register pair H-L.
    """,
    "LDA": """
        Load data from a memory address into the accumulator.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - MemoryError: If the provided memory address is not valid.

        Example:
            > LDA 2000H
            Loads the accumulator with the contents stored at the memory address 2000H.
    """,

    "STA": """
        Store the accumulator contents into a memory address.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - MemoryError: If the provided memory address is not valid.

        Example:
            > STA 2000H
            Stores the contents of the accumulator into the memory address 2000H.
    """,

    "LDAX": """
        Load the accumulator with data from the specified register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            - RpError: If the provided register pair is not valid.

        Example:
            > LDAX B
            Loads the accumulator with the contents of the memory location specified by the register pair B.
    """,

    "STAX": """
        Store the accumulator contents into the memory location specified by the register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            - RpError: If the provided register pair is not valid.

        Example:
            > STAX D
            Stores the contents of the accumulator into the memory location specified by the register pair D.
    """,

    "LHLD": """
        Load HL register pair with data from specified memory address.

        Args:
            arg (str): 16-bit memory location in hexadecimal.

        Raises:
            - MemoryError: If the provided memory address is not valid.

        Example:
            > LHLD 2000H
    """,

    "SHLD": """
        Store the content of HL register pair at the specified memory address.

        Args:
            arg (str): 16-bit memory location in hexadecimal.

        Raises:
            - MemoryError: If the provided memory address is not valid.

        Example:
            > SHLD 2000H
    """,

    "IN": """
        Input data from the specified 8-bit port location into the accumulator (A).

        Args:
            arg (str): 8-bit port location in hexadecimal.

        Raises:
            - PortError: If the port location is not valid.

        Example:
            > IN 10H
    """,

    "OUT": """
        Output data from the accumulator (A) to the specified 8-bit port location.

        Args:
            arg (str): 8-bit port location in hexadecimal.

        Raises:
            - PortError: If the port location is not valid.

        Example:
            > OUT 20H
    """,

    "XCHG": """
        Exchange the contents of the DE and HL register pairs.

        Args:
            arg (str): Not used.

        Raises:
            - NoArgumentError: If the command is followed by an argument (XCHG takes no argument).

        Example:
            > XCHG
            DE and HL register pairs after XCHG:
            DE: 12F6   HL: AB78
    """,
    "ADD": """
        Add the content of the specified register to the accumulator.

        Args:
            arg (str): The register (r) whose content will be added to the accumulator.

        Raises:
            - SyntaxError: If the syntax is incorrect or if there are additional parameters.
            - RegisterError: If the specified register (r) is not valid.

        Example:
            > ADD B
            Adds the content of register B to the accumulator.
    """,

    "ADC": """
        Add the content of the specified register or memory along with the carry to the accumulator.

        Args:
            arg (str): The register (r) or 'M' (for memory) whose content will be added to the accumulator along with the carry.

        Raises:
            - CommaError: If the ',' is missing.
            - SyntaxError: If the syntax is incorrect.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > ADC A
            Adds the content of register A along with the carry to the accumulator.
            > ADC M
            Adds the content of memory pointed to by HL along with the carry to the accumulator.
    """,

    "ADI": """
        Add immediate 8-bit data to the accumulator.

        Args:
            arg (str): The 8-bit data to be added to the accumulator.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > ADI 42H
            Adds the immediate value 42 to the accumulator.
    """,

    "DAD": """
        Add the contents of the specified register pair to the H-L register pair.

        Args:
            arg (str): The register pair (Rp) whose content will be added to the H-L register pair.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RpError: If 'Rp' is not a valid register pair.

        Example:
            > DAD B
            Adds the contents of register pair B-C to register pair H-L.
    """,

    "SUB": """
        Subtract the content of the specified register or memory from the accumulator.

        Args:
            arg (str): The register (r) or 'M' (for memory) whose content will be subtracted from the accumulator.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > SUB B
            Subtracts the content of register B from the accumulator.
            > SUB M
            Subtracts the content of memory pointed to by HL from the accumulator.
    """,

    "SUI": """
        Subtract immediate 8-bit data from the accumulator.

        Args:
            arg (str): The 8-bit data to be subtracted from the accumulator.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > SUI 42H
            Subtracts the immediate value 42 from the accumulator.
    """,

    "SBI": """
        Subtract immediate 8-bit data along with the carry from the accumulator.

        Args:
            arg (str): The 8-bit data to be subtracted along with the carry from the accumulator.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > SBI 42H
            Subtracts the immediate value 42 along with the carry from the accumulator.
    """,

    "SBB": """
        Subtract the contents of the specified register or memory along with the borrow from the accumulator.

        Args:
            arg (str): The register (r) or 'M' (for memory) whose content will be subtracted along with the borrow from the accumulator.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > SBB B
            Subtracts the content of register B along with the borrow from the accumulator.
            > SBB M
            Subtracts the content of memory pointed to by HL along with the borrow from the accumulator.
    """,
    "INR": """
        Increment the contents of the specified register or memory address.

        Args:
            arg (str): The register (r) or 'M' (for memory) whose content will be incremented.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > INR B
            Increments the content of register B.
            > INR M
            Increments the content of memory pointed to by HL.
    """,

    "INX": """
        Increment the specified register pair.

        Args:
            arg (str): The register pair (Rp) to be incremented.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RpError: If 'Rp' is not a valid register pair.

        Example:
            > INX B
            Increments the register pair B-C.
    """,

    "DCX": """
        Decrement the specified register pair.

        Args:
            arg (str): The register pair (Rp) to be decremented.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RpError: If 'Rp' is not a valid register pair.

        Example:
            > DCX B
            Decrements the register pair B-C.
    """,

    "DCR": """
        Decrement the contents of the specified register or memory address.

        Args:
            arg (str): The register (r) or 'M' (for memory) whose content will be decremented.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > DCR B
            Decrements the content of register B.
            > DCR M
            Decrements the content of memory pointed to by HL.
    """,

    "RRC": """
        Rotate the content of the accumulator from right.

        Args:
            arg (str): Not used.

        Example:
            > RRC
            Rotate the content of accumulator A from right.
    """,

    "RAR": """
        Rotate the content of the accumulator from right along with the carry flag.

        Args:
            arg (str): Not used.

        Example:
            > RAR
            Rotate the content of accumulator A from right along with the carry flag.
    """,

    "RLC": """
        Rotate the content of the accumulator from left.

        Args:
            arg (str): Not used.

        Example:
            > RLC
            Rotate the content of accumulator A from left.
    """,

    "RAL": """
        Rotate the content of the accumulator from left along with the carry flag.

        Args:
            arg (str): Not used.

        Example:
            > RAL
            Rotate the content of accumulator A from left along with the carry flag.
    """,
    "ANI": """
        Perform a bitwise AND operation between the accumulator and an immediate 8-bit data.

        Args:
            arg (str): The immediate 8-bit data to perform the AND operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > ANI 42H
            Performs bitwise AND operation between the accumulator and 42H.
    """,

    "ORI": """
        Perform a bitwise OR operation between the accumulator and an immediate 8-bit data.

        Args:
            arg (str): The immediate 8-bit data to perform the OR operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > ORI 3AH
            Performs bitwise OR operation between the accumulator and 3AH.
    """,

    "XRI": """
        Perform a bitwise XOR operation between the accumulator and an immediate 8-bit data.

        Args:
            arg (str): The immediate 8-bit data to perform the XOR operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - DataError: If the parameter is not a valid 8-bit data.

        Example:
            > XRI FFH
            Performs bitwise XOR operation between the accumulator and FFH.
    """,

    "ANA": """
        Perform a bitwise AND operation between the accumulator and a register or memory content.

        Args:
            arg (str): The register (r) or 'M' (for memory) to perform the AND operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > ANA B
            Performs bitwise AND operation between the accumulator and register B.
            > ANA M
            Performs bitwise AND operation between the accumulator and memory content pointed by HL.
    """,

    "ORA": """
        Perform a bitwise OR operation between the accumulator and a register or memory content.

        Args:
            arg (str): The register (r) or 'M' (for memory) to perform the OR operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > ORA B
            Performs bitwise OR operation between the accumulator and register B.
            > ORA M
            Performs bitwise OR operation between the accumulator and memory content pointed by HL.
    """,

    "XRA": """
        Perform a bitwise XOR operation between the accumulator and a register or memory content.

        Args:
            arg (str): The register (r) or 'M' (for memory) to perform the XOR operation with.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register or 'M'.

        Example:
            > XRA B
            Performs bitwise XOR operation between the accumulator and register B.
            > XRA M
            Performs bitwise XOR operation between the accumulator and memory content pointed by HL.
    """,

    "CMA": """
        Complement the contents of the accumulator (bitwise NOT operation).

        Args:
            arg (str): Not used.

        Example:
            > CMA
            Complements the contents of the accumulator (bitwise NOT operation).
    """,

    "STC": """
        Set the carry flag in the accumulator.

        Args:
            arg (str): Not used.

        Example:
            > STC
            Sets the carry flag in the accumulator.
    """,
    "PUSH": """
        Push the contents of the specified register pair onto the stack.

        Args:
            arg (str): The register pair to push onto the stack.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register pair.

        Example:
            > PUSH B
            Pushes the contents of register pair BC onto the stack.
    """,

    "POP": """
        Pop the contents from the stack into the specified register pair.

        Args:
            arg (str): The register pair to pop from the stack.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - RegisterError: If the parameter is not a valid register pair.

        Example:
            > POP H
            Pops the contents from the stack into register pair HL.
    """,

    "XTHL": """
        Exchange the contents of HL register pair with the contents of the top of the stack.

        Args:
            arg (str): Not used.

        Example:
            > XTHL
            Exchanges the contents of HL register pair with the contents of the top of the stack.
    """,

    "SPHL": """
        Load the stack pointer with the contents of HL register pair.

        Args:
            arg (str): Not used.

        Example:
            > SPHL
            Loads the stack pointer with the contents of HL register pair.
    """,

    "PCHL": """
        Jump to the memory address specified by HL register pair.

        Args:
            arg (str): Not used.

        Example:
            > PCHL
            Jumps to the memory address specified by HL register pair.
    """,

    "JMP": """
        Unconditional jump to the specified memory address.

        Args:
            arg (str): The memory address to jump to.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JMP 2000H
            Unconditionally jumps to the memory address 2000H.
    """,

    "JC": """
        Conditional jump to the specified memory address if carry flag is set.

        Args:
            arg (str): The memory address to jump to if carry flag is set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JC 3000H
            Jumps to the memory address 3000H if the carry flag is set.
    """,

    "JNC": """
        Conditional jump to the specified memory address if carry flag is not set.

        Args:
            arg (str): The memory address to jump to if carry flag is not set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JNC 4000H
            Jumps to the memory address 4000H if the carry flag is not set.
    """,

    "JZ": """
        Conditional jump to the specified memory address if zero flag is set.

        Args:
            arg (str): The memory address to jump to if zero flag is set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JZ 5000H
            Jumps to the memory address 5000H if the zero flag is set.
    """,

    "JNZ": """
        Conditional jump to the specified memory address if zero flag is not set.

        Args:
            arg (str): The memory address to jump to if zero flag is not set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JNZ 6000H
            Jumps to the memory address 6000H if the zero flag is not set.
    """,

    "JM": """
        Conditional jump to the specified memory address if sign flag is set (negative).

        Args:
            arg (str): The memory address to jump to if sign flag is set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JM 7000H
            Jumps to the memory address 7000H if the sign flag is set (negative).
    """,

    "JP": """
        Conditional jump to the specified memory address if sign flag is not set (positive).

        Args:
            arg (str): The memory address to jump to if sign flag is not set.

        Raises:
            - SyntaxError: If there are insufficient parameters.
            - MemoryError: If the parameter is not a valid memory address.

        Example:
            > JP 8000H
            Jumps to the memory address 8000H if the sign flag is not set (positive).
    """,

        "CALL": """
            Call a subroutine at the specified memory address.

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CALL 2000H
                Calls the subroutine at memory address 2000H.
        """,

        "CC": """
            Conditional call: Call a subroutine at the specified memory address if the carry flag is set (CY=1).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CC 2000H
                Calls the subroutine at memory address 2000H if the carry flag is set.
        """,

        "CZ": """
            Conditional call: Call a subroutine at the specified memory address if the zero flag is set (Z=1).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CZ 2000H
                Calls the subroutine at memory address 2000H if the zero flag is set.
        """,

        "CNZ": """
            Conditional call: Call a subroutine at the specified memory address if the zero flag is reset (Z=0).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CNZ 2000H
                Calls the subroutine at memory address 2000H if the zero flag is reset.
        """,

        "CM": """
            Conditional call: Call a subroutine at the specified memory address if the sign flag is set (S=1).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CM 2000H
                Calls the subroutine at memory address 2000H if the sign flag is set.
        """,

        "CP": """
            Conditional call: Call a subroutine at the specified memory address if the sign flag is reset (S=0).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CP 2000H
                Calls the subroutine at memory address 2000H if the sign flag is reset.
        """,

        "CPE": """
            Conditional call: Call a subroutine at the specified memory address if the parity flag is set (P=1).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CPE 2000H
                Calls the subroutine at memory address 2000H if the parity flag is set.
        """,

        "CPO": """
            Conditional call: Call a subroutine at the specified memory address if the parity flag is reset (P=0).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CPO 2000H
                Calls the subroutine at memory address 2000H if the parity flag is reset.
        """,

        "CNC": """
            Conditional call: Call a subroutine at the specified memory address if the carry flag is reset (CY=0).

            Args:
                arg (str): The memory address (in hexadecimal) to call.

            Raises:
                - SyntaxError: If there are insufficient parameters.
                - MemoryError: If the provided memory address is restricted or not valid.

            Example:
                > CNC 2000H
                Calls the subroutine at memory address 2000H if the carry flag is reset.
        """,

        "RET": """
            Return from subroutine.

            Args: None

            Example:
                > RET
                Returns from the current subroutine.
        """,

        "RC": """
            Conditional return: Return from subroutine if the carry flag is set (CY=1).

            Args: None

            Example:
                > RC
                Returns from the current subroutine if the carry flag is set.
        """,

        "RZ": """
            Conditional return: Return from subroutine if the zero flag is set (Z=1).

            Args: None

            Example:
                > RZ
                Returns from the current subroutine if the zero flag is set.
        """,

        "RNZ": """
            Conditional return: Return from subroutine if the zero flag is reset (Z=0).

            Args: None

            Example:
                > RNZ
                Returns from the current subroutine if the zero flag is reset.
        """,

        "RM": """
            Conditional return: Return from subroutine if the sign flag is set (S=1).

            Args: None

            Example:
                > RM
                Returns from the current subroutine if the sign flag is set.
        """,

        "RP": """
            Conditional return: Return from subroutine if the sign flag is reset (S=0).

            Args: None

            Example:
                > RP
                Returns from the current subroutine if the sign flag is reset.
        """,

        "RPE": """
            Conditional return: Return from subroutine if the parity flag is set (P=1).

            Args: None

            Example:
                > RPE
                Returns from the current subroutine if the parity flag is set.
        """,

        "RPO": """
            Conditional return: Return from subroutine if the parity flag is reset (P=0).

            Args: None

            Example:
                > RPO
                Returns from the current subroutine if the parity flag is reset.
        """,

        "RNC": """
            Conditional return: Return from subroutine if the carry flag is reset (CY=0).

            Args: None

            Example:
                > RNC
                Returns from the current subroutine if the carry flag is reset.
        """,

        "exam memory":"""
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
        """,

        "exam port":"""
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
        """,
        "exam register":"""
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
        """,
        "exam flag":"""
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
        """,
        "exam stack": """
        Display stack addresses and their contents.

        Args:
            arg (str): Comma-separated list of stack memory addresses.

        Raises:
            KeyError: If the provided stack memory address is invalid.

        Example:
            > exam stack 5000H, 6000H, 7000H
            +-------+--------+
            | Index | Content|
            +-------+--------+
            |  5000H|   ...  |
            |  6000H|   ...  |
            |  7000H|   ...  |
            +-------+--------+
        """
}