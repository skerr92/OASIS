# ADI

## Summary

Adds a 16-bit immediate to ra.

## Syntax

```asm
ADI ra, imm16
```

## Encoding

Class: `00`

Opcode: `0001`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | destination/source register |
| `19:16` | `reserved` | must be zero |
| `15:0` | `imm16` | immediate operand |

## Operation

```text
ra = ra + imm16
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Overflow wraps modulo 2^16
- reserved bits must be zero.

## Example

```asm
MVI r1, 0x0100
ADI r1, 4
```
