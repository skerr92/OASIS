# RTR

## Summary

Rotates ra right by an immediate amount.

## Syntax

```asm
RTR ra, imm6
```

## Encoding

Class: `01`

Opcode: `1000`

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
ra = rotate_right(ra, imm6 mod 16)
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Rotate amount is reduced modulo 16
- rotate by zero leaves ra unchanged
- reserved bits must be zero.

## Example

```asm
MVI r1, 0x0001
RTR r1, 1
```
