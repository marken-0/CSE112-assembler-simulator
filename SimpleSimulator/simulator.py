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
