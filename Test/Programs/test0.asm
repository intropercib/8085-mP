START: 
MVI A,30H
MVI B,40H
CALL INIT_VALUES; Call subroutine to initialize memory
MOV C, A
HLT             ; Halt the processor

INIT_VALUES:            ; Subroutine to initialize memory locations
ADD B
RET