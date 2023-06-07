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
            
    return (0,0)

def isLabelValid(lbl_called,lbl_declared,lbl_inst,inst,alphanum,lbl_declared2,var_declared2):

    numarr = ['0','1','2','3','4','5','6','7','8','9']
    inst2 = inst.copy()
    inst2.append('var')
    l1 = len(lbl_declared)
    l2 = len(lbl_inst)
    if l1!=l2:
        return (-5,0)
    count2 = 0
    for i in lbl_declared:
        a = i[0]
        b = len(a)
        count = 0
        count4 = 0
        for j in a:
            if j in alphanum:
                count+=1
            if j in numarr:
                count4+=1
        if count!=b:
            return (-1,i[1])
        if b==count4:
            return (-6,i[1])
        else:
            c = lbl_inst[count2]
            if isLineValid2(c)!=0 or lineTypesMatch(c,lbl_declared2,var_declared2)!=0:
                return (-2,i[1])
        count2+=1
    lbl2 = []
    for i in lbl_declared:
        lbl2.append(i[0])
    for i in lbl_called:
        if i not in lbl2:
            return (-3,i)     
    for i in lbl2:
        if i in inst2:
            return (-4,i)
    return (0,0)
def lineTypesMatch(line_comp,lbl_declared2,var_declared2):
    if line_comp[0]=="mov":
        tmp = "movi" if "$" in line_comp[-1] else "movr"
    else:
        tmp = line_comp[0]

    ls_type_order = type_to_members[opcodeTable[tmp][-1]]
    for i, val in enumerate(line_comp[1:], start=1):
        if ls_type_order[i] == 'Register':
            if isRegisterValid(val) == -1:
                if line_comp[0] != "movr":
                    return -4
            elif isRegisterValid(val) is False:
                return -1
        elif ls_type_order[i] == 'Immediate' and not isImmediateValid(val):
            return -2
        elif ls_type_order[i] == 'Immediate' and not isImmediateRangeValid(val):
            return -3

    if ls_type_order[-1] == 'Memory Address':
        if line_comp[0] in ('ld', 'st') and line_comp[-1] not in var_declared2:
            return (-6 if line_comp[-1] not in lbl_declared2 else -5)
        elif line_comp[0] in ('jmp', 'jlt', 'jgt', 'je') and line_comp[-1] not in lbl_declared2:
            return (-8 if line_comp[-1] in var_declared2 else -7)
    return 0
def Duplication(lbl_declared,var_declared,lbl_declared2,var_declared2):
    """Checks if there are any Duplicate Labels or Variables"""
    a = len(lbl_declared)
    b = len(var_declared)
    for i in var_declared2:
        if i in lbl_declared2:
            return (-1,i)
    for i in range(0,a):
        a2 = lbl_declared[i][0]
        for j in range(i+1,a):
            if a2==lbl_declared[j][0]:
                return (-2,a2)
    for i in range(0,b):
        b2 = var_declared[i][0]
        for j in range(i+1,b):
            if b2==var_declared[j][0]:
                return (-3,var_declared[j][1])
    return (0,0)
