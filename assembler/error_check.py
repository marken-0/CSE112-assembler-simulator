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

def isVarValid(var_declared,var_called,alphanum,inst):
    """Checks if Variables are Valid"""
    numarr = ['0','1','2','3','4','5','6','7','8','9']
    inst2 = inst.copy()
    inst2.append('var')
    len1 = len(var_declared)
    for i in var_declared:
        if i[1]!=1:
            return (-1,i[1])
        if i[1]==1:
            a = i[0]
            b = len(a)
            count = 0
            count2 = 0
            for j in a:
                if j in alphanum:
                    count+=1
                if j in numarr:
                    count2+=1
            if count!=b:
                return (-2,i[0])
            if b==count2:
                return (-5,i[0])
    b2 = len(var_called)
    var2 = []
    for i in var_declared:
        var2.append(i[0])
    for i in var2:
        if i in inst2:
            return (-4,i)
    
    for i in var_called:
        if i not in var2:
            return (-3,i)
            
    return (0,0)
