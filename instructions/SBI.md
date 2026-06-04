# SBI

## Summary

Subtracts a 16-bit immediate from ra.

## Syntax

```asm
SBI ra, imm16
```

## Encoding

Class: `00`

Opcode: `0010`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | destination/source register |
| `19:16` | `reserved` | must be zero |
| `15:0` | `imm16` | immediate operand |

## Operation

```text
ra = ra - imm16
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Underflow wraps modulo 2^16
- reserved bits must be zero.

## Example

```asm
MVI r56, 0x01ff
SBI r56, 1
```
