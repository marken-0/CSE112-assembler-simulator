from ISA import *

def isInstructionValid(instruction):
    for i in range(len(instructions)):
        if instruction == instructions[i]:
            return True
    return False
def isInstructionValid2(instruction):
    for i in range(len(instructions_original)):
        if instruction == instructions_original[i]:
            return True
    return False
def isRegisterValid(register_):
    for i in range(len(register_list)):
        if register_ == register_list[i]:
            if register_ == "FLAGS":
                return -1
            else:
                return True
    return False
def isImmediateValid(immediate):
    if not immediate.startswith('$'):
        return False
    if not immediate[1:].isdigit():
        return False
    return True
def isImmediateRangeValid(immediate):
    val = int(immediate[1:])
    if val >= 0 and val <= 255: return True
    return False
def isSizeRight(instruction, ls):
    size = len(ls)
    if instruction == "mov":
        if size == 3:
            return True
    else:
        type_instruction = 0
        for key in opcodeTable:
            if instruction == key:
                type_instruction = opcodeTable[key][1]
                break

        if size == type_to_input_len[type_instruction]:
            return True
    return False
def isLineValid(line_comp):
    if not isInstructionValid(line_comp[0]): return -1
    if not isSizeRight(line_comp[0], line_comp): return -2
    return 0
def isLineValid2(line_comp):
    if not isInstructionValid2(line_comp[0]):
        return -1
    if not isSizeRight(line_comp[0], line_comp):
        return -2
    return 0
