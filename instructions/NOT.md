# NOT

## Summary

Inverts every bit in ra.

## Syntax

```asm
NOT ra
```

## Encoding

Class: `01`

Opcode: `1010`

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
ra = ~ra
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Reserved bits must be zero.

## Example

```asm
MVI r1, 0x00ff
NOT r1
```
