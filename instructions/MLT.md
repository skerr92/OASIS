# MLT

## Summary

Multiplies ra by rb and keeps the low 16 bits.

## Syntax

```asm
MLT ra, rb
```

## Encoding

Class: `01`

Opcode: `1011`

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
ra = low16(ra * rb)
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Product truncates to 16 bits
- reserved bits must be zero.

## Example

```asm
MVI r1, 7
MVI r2, 6
MLT r1, r2
```
