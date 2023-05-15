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

