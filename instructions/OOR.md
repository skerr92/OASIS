# OOR

## Summary

Computes the bitwise OR of ra and rb.

## Syntax

```asm
OOR ra, rb
```

## Encoding

Class: `01`

Opcode: `0100`

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
ra = ra | rb
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Mnemonic is OOR to avoid ambiguity with assembler keywords
- reserved bits must be zero.

## Example

```asm
MVI r1, 0x00f0
MVI r2, 0x0f00
OOR r1, r2
```
