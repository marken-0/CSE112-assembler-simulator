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
