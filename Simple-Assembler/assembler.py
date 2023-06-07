from ISA import *
from error_check import *
import sys
################################################
def float_to_bin(num):
    exponent_bits = 3
    mantissa_bits = 5

    if num == 0: return "0" * (exponent_bits + mantissa_bits)

    exponent = 0
    while num >= 2 or num < 1:
        if num >= 2:
            num /= 2
            exponent += 1
        else:
            num *= 2
            exponent -= 1

    exponent += 2 ** (exponent_bits - 1) - 1
    exponent_binary = format(exponent, f"0{exponent_bits}b")

    num -= 1
    mantissa_binary = ""
    for _ in range(mantissa_bits):
        num *= 2
        mantissa_binary += str(int(num))
        num -= int(num)

    return exponent_binary + mantissa_binary

ls_inputs = []
# inputFile = 'input.txt'
# with open(inputFile, "r") as file:
#     for line in file:
#         input_line = line.strip()
#         if input_line == '':
#             continue
#         ls_inputs.append(input_line)


for line in sys.stdin:
    input_line = line.strip()
    if input_line == '':
        continue
    ls_inputs.append(input_line)


################################################

declaredLabels_idx = []
declaredLabels = []
lblInstruction = []
tmp_idx = 0
for line in ls_inputs:
    tokens = line.strip().split()
    
    if tokens and tokens[0].endswith(":"):
        label_name = tokens[0][:-1]
        declaredLabels.append(label_name)
        declaredLabels_idx.append((label_name, tmp_idx))
        
        if len(tokens) > 1: lblInstruction.append(tokens[1:])
    tmp_idx += 1
    
################################################

calledLabels_idx = []
calledLabels2 = []
calledVars = []
calledVars2 = []

tmp_idx = 0
for tmp_idx, line in enumerate(ls_inputs):
    tokens = line.strip().split()
    
    if tokens and tokens[0].endswith(":") and len(tokens) > 1:
        if tokens[1] in ['ld', 'st']:
            calledVars.append(tokens[-1])
            calledVars2.append([tokens[-1], tmp_idx])
        elif tokens[1] in ['jmp', 'jlt', 'jgt', 'je']:
            calledLabels_idx.append(tokens[-1])
            calledLabels2.append([tokens[-1], tmp_idx])
    
    elif tokens and tokens[0] in ['ld', 'st']:
        calledVars.append(tokens[-1])
        calledVars2.append([tokens[-1], tmp_idx])
    elif tokens and tokens[0] in ['jmp', 'jlt', 'jgt', 'je']:
        calledLabels_idx.append(tokens[-1])
        calledLabels2.append([tokens[-1], tmp_idx])

################################################

errors = []
for i, line in enumerate(ls_inputs):
    tokens = line.strip().split()
    
    # if tokens[0] == 'movi' or tokens[0] == 'movr':
    #     errors.append(f'ERROR: No Such Instruction Found as {tokens[0]} for instruction {i+1}')
    if tokens[0] == 'mov':
        if len(tokens) < 2:
            errors.append(f'ERROR at line number {i+1}: invalid arguments for mov')
            break
        if tokens[1] == 'FLAGS':
            errors.append(f'ERROR at line number {i+1}: flags cannot be used as a source register')
        tokens[0] = 'movi' if tokens[-1][0] == '$' else 'movr'
    
    ls_inputs[i] = ' '.join(tokens)

declaredVars = []
declaredVars2 = []


tmp_idx = 1
for line in ls_inputs:
    tokens = line.strip().split()

    if tokens[0] == "var":
        if len(tokens) == 2:
            var_name = tokens[1]
            declaredVars.append((var_name, tmp_idx))
            declaredVars2.append(var_name)
            tmp_idx -= 1
        else:
            errors.append('ERROR: more than 2 arguments in declaration of variables')

    tmp_idx += 1
    
   
################################################

error_messages = {
    -1: 'Illegal declaration of variables',
    -2: 'Variable name incorrect',
    -3: 'Variable called was never declared',
    -4: 'Variable has the same name as an ISA instruction',
    -5: 'Variable name incorrect'
}

varCheck = isVarValid(declaredVars, calledVars, alphanum, instructions_registers)

if varCheck[0] in error_messages:
    index = 0
    if varCheck[0] == -2 or varCheck[0] == -4 or varCheck[0] == -5:
        index = next((i for i, var in enumerate(declaredVars2) if var == varCheck[1]), 0)
    elif varCheck[0] == -3:
        index = next((var[1] for var in calledVars2 if var[0] == varCheck[1]), 0)
    
    errors.append(error_messages[varCheck[0]].format(index + 1))
    VALID = False
    
################################################

error_messages2 = {
        -1: 'ERROR in line {0}: Invalid label name',
        -2: 'ERROR in line {0}: Invalid label instruction',
        -3: 'ERROR in line {0}: Invalid label called',
        -4: 'ERROR in line {0}: Label name is the same as an instruction name',
        -5: 'ERROR in line {0}: Label instruction not given',
        -6: 'ERROR in line {0}: Invalid label name (only numeric or empty)'
    }

validlbl = isLabelValid(calledLabels_idx,declaredLabels_idx,lblInstruction,instructions_registers,alphanum,declaredLabels,declaredVars2)

if validlbl[0] in error_messages2:
    index = 0
    if validlbl[0] == -3:
        index = next((i for i, (lbl, _) in enumerate(calledLabels2) if lbl == validlbl[1]), None)
    elif validlbl[0] == -4:
        index = next((i for i, lbl in enumerate(declaredLabels_idx) if lbl == validlbl[1]), None)

    errors.append(error_messages2[validlbl[0]].format(index + 1))
    VALID = False

################################################

duplicationCheck = Duplication(declaredLabels_idx,declaredVars,declaredLabels,declaredVars2)

if duplicationCheck[0] == -1:
    index = declaredVars2.index(duplicationCheck[1])
    errors.append(f'ERROR in line {index + 1}: Label name is the same as a variable')
    VALID = False

if duplicationCheck[0] == -2:
    index = declaredLabels_idx[0].index(duplicationCheck[1])
    errors.append(f'ERROR in line {index + 1}: A label was declared more than once')
    VALID = False

if duplicationCheck[0] == -3:
    errors.append(f'ERROR in line {duplicationCheck[1] + 1}: A variable was declared more than once')
    VALID = False


###############################################
HLT_COUNT = 0

error_messages3 = {
    -1: 'No Such Instruction Found',
    -2: 'Wrong Syntax used, incorrect number of arguments',
    -3: 'Invalid Register (No such Register Found)',
    -4: 'Illegal Immediate Value used',
    -5: 'Invalid use of FLAGS register',
    -6: 'Invalid use of label',
    -7: 'Invalid use of variable',
    -8: 'Invalid use of label'
}

for i, line in enumerate(ls_inputs):
    line = line.strip()
    tokens = list(map(str, line.split()))
    opcode = tokens[0]

    if opcode.endswith(':'):
        if tokens[-1] == 'hlt':
            HLT_COUNT += 1
        continue

    if opcode == 'var':
        continue

    line_valid = isLineValid(tokens)
    if line_valid == -1 or line_valid == -2:
        errors.append(f'ERROR in line {i+1}: {error_messages[line_valid]}')
        VALID = False
        break

    line_match = lineTypesMatch(tokens, declaredLabels, declaredVars2)
    if line_match in [-1, -2, -3, -4, -5, -6, -7, -8]:
        errors.append(f'ERROR in line {i+1}: {error_messages3[line_match]}')
        VALID = False
        break

    if 'hlt' in tokens:
        HLT_COUNT += 1


if HLT_COUNT == 0:
    errors.append('ERROR: hlt not present')
    VALID = False

if HLT_COUNT > 1:
    errors.append('ERROR: multiple hlt present')
    VALID = False

if HLT_COUNT == 1:
    last_line = ls_inputs[-1].strip()
    last_line_comp = list(map(str, last_line.split()))

    if last_line_comp[-1] != 'hlt':
        errors.append('ERROR: hlt is not the last instruction')
        VALID = False
    elif last_line_comp[0].endswith(':'):
        label = last_line_comp[0][:-1]
        if label not in calledLabels_idx:
            errors.append('ERROR: hlt is not the last instruction, given label not called')
            VALID = False

################################################
output = []
if len(errors) == 0:
    len_without_vars_and_labels = sum(1 for inst in ls_inputs if not inst.strip().startswith('var'))

    ls_vars = [[i, inst.split()[-1]] for i, inst in enumerate(ls_inputs) if 'var' in inst]
    ls_labels = [[i, inst.split(':')[0]] for i, inst in enumerate(ls_inputs) if ':' in inst]

    no_of_vars = len(ls_vars)

    for inst in ls_inputs:
        inst_comps = inst.strip().split()

        if inst_comps[0] == 'var':
            continue

        if inst_comps[0][-1] == ":":
            inst_comps = inst_comps[1:]

        temp = "movi" if inst_comps[0] == "mov" and "$" in inst_comps[-1] else inst_comps[0]
        inst_type = opcodeTable[temp][-1]
        output_string = opcodeTable[temp][0] + '0' * type_to_unusedbits[inst_type]

        for comp in inst_comps[1:1+type_to_reg_no[inst_type]]:
            output_string += register_to_encoding[comp]

        if inst_type == 'B':
            imm = int(inst_comps[-1][1:])
            output_string += bin(imm)[2:].zfill(7)

        if inst_type == 'Bf':
            imm = float(inst_comps[-1][1:])
            output_string += float_to_bin(imm)

        if inst_type == 'D':
            location = len_without_vars_and_labels + sum(i[0] for i in ls_vars if i[-1] == inst_comps[-1])
            output_string += bin(location)[2:].zfill(7)

        if inst_type == 'E':
            location = sum(i[0] - no_of_vars for i in ls_labels if i[-1] == inst_comps[1])
            output_string += bin(location)[2:].zfill(7)
        
        output.append(output_string)


else:
    output.append(errors[0])

# outputFile = 'output.txt'
# with open(outputFile, 'w') as f:
#     f.write('\n'.join(output))

print('\n'.join(output))



