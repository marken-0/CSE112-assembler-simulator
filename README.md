# Custom Assembler Simulator
Project for CSE112 (Computer organnisation). Making a Custom Assemler Simulator for a given ISA.
Each Instruction is 16 bits long
## Instruction Set (Bonus)

| Instruction | OPCODE | Semantics | Syntax | Type |
|-------------|--------|-----------|--------|------|
| Power   | 10011  | Calculates the power of one register to another and stores the result in a destination register. If the result exceeds 16 bits, it overflows and sets a flag register. | pow rd rs1 rs2 | A |
| Square Root  | 10100  | Calculates the square root of a register value and stores the result in a destination register. If the result is less than 1, it overflows and sets a flag register. | sqrt rd rs1 | C |
| Add Imm  | 10101  | Adds an immediate value to a register and stores the result in the same register. If the result exceeds 16 bits, it overflows and sets a flag register. | addi rd imm | B |
| Sub Imm  | 10110  | Subtracts an immediate value from a register and stores the result in the same register. If the result is negative, it overflows and sets a flag register. | subi rd imm | B |

## Instruction Details

### pow_10011

- OPCODE: 10011
- Semantics: Calculates the power of one register to another and stores the result in a destination register. If the result exceeds 16 bits, it overflows and sets a flag register.
- Syntax: `pow rd rs1 rs2`
- Type: A

### sqrt_10100

- OPCODE: 10100
- Semantics: Calculates the square root of a register value and stores the result in a destination register. If the result is less than 1, it overflows and sets a flag register.
- Syntax: `sqrt rd rs1`
- Type: C

### addi_10101

- OPCODE: 10101
- Semantics: Adds an immediate value to a register and stores the result in the same register. If the result exceeds 16 bits, it overflows and sets a flag register.
- Syntax: `addi rd imm`
- Type: B

### subi_10110

- OPCODE: 10110
- Semantics: Subtracts an immediate value from a register and stores the result in the same register. If the result is negative, it overflows and sets a flag register.
- Syntax: `subi rd imm`
- Type: B

