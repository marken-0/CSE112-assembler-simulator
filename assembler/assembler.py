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