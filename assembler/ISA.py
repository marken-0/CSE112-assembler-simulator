# NUM_INSTRUCTIONS = 20
# NUM_REGS = 8
# NUM_TYPES = 6
# OP_CODE_SIZE = 5
# REGISTER_SIZE = 3
# MEMORY_ADDRESS_SIZE = 8
# IMMEDIATE_SIZE = 8
# LABEL_LENGTH = 30
# MAX_LINE_LENGTH = 100
# err = 0

instructions = ["add", "sub", "movi", "movr", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
instructions_original = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
instructions_registers = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt", "R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
register_list = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
numarr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphanum = ['_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

opcodeTable = {
    'add': ['00000', 'A'],
    'sub': ['00001', 'A'],
    'movi': ['00010', 'B'],
    'movr': ['00011', 'C'],
    'ld': ['00100', 'D'],
    'st': ['00101', 'D'],
    'mul': ['00110', 'A'],
    'div': ['00111', 'C'],
    'rs': ['01000', 'B'],
    'ls': ['01001', 'B'],
    'xor': ['01010', 'A'],
    'or': ['01011', 'A'],
    'and': ['01100', 'A'],
    'not': ['01101', 'C'],
    'cmp': ['01110', 'C'],
    'jmp': ['01111', 'E'],
    'jlt': ['11100', 'E'],
    'jgt': ['11101', 'E'],
    'je': ['11111', 'E'],
    'hlt': ['11010', 'F']
}
