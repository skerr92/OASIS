# SHL

## Summary

Shifts ra left by an immediate amount.

## Syntax

```asm
SHL ra, imm6
```

## Encoding

Class: `01`

Opcode: `0111`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `01` ALU/jump class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | destination/source register |
| `19:14` | `rb/imm6` | source register or shift/rotate amount |
| `13:6` | `target8` | jump target for branch instructions |
| `5:0` | `reserved` | must be zero |

## Operation

```text
ra = ra << (imm6 mod 16)
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Shift amount is reduced modulo 16
- reserved bits must be zero.

## Example

```asm
MVI r1, 0x0001
SHL r1, 4
```
