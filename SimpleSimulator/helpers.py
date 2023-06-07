from ISA import *

def to_bin(num, bits): return bin(num).replace("0b","").zfill(bits)

def to_dec(num): return int(num, 2)

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

def bin_to_float(binary):
    exponent_bits = 3
    mantissa_bits = 5
    binary = binary[-8:]
    if binary == "0" * (exponent_bits + mantissa_bits):
        return 0.0

    exponent_binary = binary[:exponent_bits]
    mantissa_binary = binary[exponent_bits:]

    exponent = int(exponent_binary, 2)
    exponent -= 2 ** (exponent_bits - 1) - 1

    mantissa = 1 
    for i, bit in enumerate(mantissa_binary):
        mantissa += int(bit) * (2 ** -(i + 1))

    float_value = mantissa * (2 ** exponent)
    return float_value


def reg_values():
    for i in REG.values():
        if len(i) == 16: print(i, end = ' ')
        else:
            tmp = to_dec(i)
            print(to_bin(tmp, 16), end = ' ')

def add_00000(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x + y, 16)
    if len(REG[rd]) > 16:
        REG[rd] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else: REG['111'] = to_bin(0, 16)

def sub_00001(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x - y, 16)
    if (x - y) < 0:
        REG[rd] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else: REG['111'] = to_bin(0, 16)

def movi_00010(rd, imm):
    REG[rd] = to_bin(imm, 16)
    REG['111'] = to_bin(0, 16)

def movr_00011(rd, rs1):
    REG[rd] = REG[rs1]
    REG['111'] = to_bin(0, 16)

def ld_00100(rd, mem):
    if mem not in MEM:
        MEM[mem] = to_bin(0, 16)
    REG[rd] = MEM[mem]
    REG['111'] = to_bin(0, 16)

def st_00101(rd, mem):
    MEM[mem] = REG[rd]
    REG['111'] = to_bin(0, 16)

def mul_00110(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x * y, 16)
    if len(REG[rd]) > 16:
        REG[rd] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else: REG['111'] = to_bin(0, 16)

def div_00111(rd, rs1):
    x = to_dec(REG[rd])
    y = to_dec(REG[rs1])
    if y == 0:
        REG[rd] = to_bin(0, 16)
        REG[rs1] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else:
        REG[rd] = to_bin(x // y, 16)
        REG[rs1] = to_bin(x % y, 16)
        REG['111'] = to_bin(0, 16)

def rs_01000(rd, imm):
    x = to_dec(REG[rd])
    REG[rd] = to_bin(x >> imm, 16)
    REG['111'] = to_bin(0, 16)

def ls_01001(rd, imm):
    x = to_dec(REG[rd])
    REG[rd] = to_bin(x << imm, 16)
    REG['111'] = to_bin(0, 16)

def xor_01010(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x ^ y, 16)
    REG['111'] = to_bin(0, 16)

def or_01011(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x | y, 16)
    REG['111'] = to_bin(0, 16)
    
def and_01100(rd, rs1, rs2):
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    REG[rd] = to_bin(x & y, 16)
    REG['111'] = to_bin(0, 16)

def not_01101(rd, rs1):
    x = to_dec(REG[rs1])
    REG[rd] = to_bin(~x, 16)
    REG['111'] = to_bin(0, 16)

def cmp_01110(rs1, rs2):
    REG['111'] = to_bin(0, 16)
    x = to_dec(REG[rs1])
    y = to_dec(REG[rs2])
    if x == y: REG['111'] = to_bin(1, 16)
    elif x > y: REG['111'] = to_bin(2, 16)
    elif x < y: REG['111'] = to_bin(4, 16)

def addf_10000(rd, rs1, rs2):
    x = bin_to_float(REG[rs1])
    y = bin_to_float(REG[rs2])
    REG[rd] = float_to_bin(x + y).zfill(16)
    if len(REG[rd]) > 16:
        REG[rd] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else: REG['111'] = to_bin(0, 16)

def subf_10001(rd, rs1, rs2):
    x = bin_to_float(REG[rs1])
    y = bin_to_float(REG[rs2])
    REG[rd] = float_to_bin(x - y).zfill(16)
    if (x - y) < 0:
        REG[rd] = to_bin(0, 16)
        REG['111'] = to_bin(8, 16)
    else: REG['111'] = to_bin(0, 16)
 
def movf_10010(rd, imm):
    REG[rd] = to_bin(imm, 16)
    REG['111'] = to_bin(0, 16)

