import sys
from helpers import *
from ISA import *

PC = 0
input_list = []
def exe_inst(inst):
    opcode = inst[:5]
    if opcode in opcode_to_inst:
        func = opcode_to_inst[opcode]
        if opcode in type_to_opcode["A"]:
            rd = inst[7:10]
            rs1 = inst[10:13]
            rs2 = inst[13:]
            func(rd, rs1, rs2)
        elif opcode in type_to_opcode["B"]:
            r1 = inst[6:9]
            imm = to_dec(inst[9:])
            func(r1, imm)
        elif opcode in type_to_opcode["Bf"]:
            r1 = inst[5:8]
            imm = to_dec(inst[8:])
            func(r1, imm)
        elif opcode in type_to_opcode["C"]:
            r1 = inst[10:13]
            r2 = inst[13:]
            func(r1, r2)
        elif opcode in type_to_opcode["D"]:
            r1 = inst[6:9]
            mem = inst[9:]
            func(r1, mem)

for line in sys.stdin:
    input_line = line.strip()
    if input_line == '':
        continue
    input_list.append(input_line)

while input_list[PC] != '1101000000000000':
    opcode = input_list[PC][:5]
    print(to_bin(PC, 7), end = '        ')
    if (opcode not in type_to_opcode["E"] and opcode not in type_to_opcode["F"]):
        exe_inst(input_list[PC])
        reg_values()
        PC += 1            
    else:
        mem = int(input_list[PC][8:], 2)
        if opcode == "01111": PC = mem
        elif opcode == "11100":
            PC = mem if REG["111"] == to_bin(4, 16) else PC + 1
        elif opcode == "11101":
            PC = mem if REG["111"] == to_bin(2, 16) else PC + 1
        elif opcode == "11111":
            PC = mem if REG["111"] == to_bin(1, 16) else PC + 1
        REG["111"] = to_bin(0, 16)
        reg_values()

    print()     

    
REG["111"] = to_bin(0, 16)
print(to_bin(PC, 7), end = '        ')
reg_values()
print()

for i in range (0,128):
    if(i < len(input_list)):
        print(input_list[i])
    else:
        if(to_bin(i, 7) in MEM.keys()):
            print(MEM[to_bin(i, 7)])
        else:
            print("0000000000000000")
