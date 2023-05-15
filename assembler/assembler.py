from ISA import *
from error_check import *
################################################

ls_inputs = []
inputFile = 'input.txt'
with open(inputFile, "r") as file:
    for line in file:
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
    -1: 'ERROR in line {0}: Illegal declaration of variables',
    -2: 'ERROR in line {0}: Variable name incorrect',
    -3: 'ERROR in line {0}: Variable called was never declared',
    -4: 'ERROR in line {0}: Variable has the same name as an ISA instruction',
    -5: 'ERROR in line {0}: Variable name incorrect'
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


