# MVI

## Summary

Loads a 16-bit immediate into ra.

## Syntax

```asm
MVI ra, imm16
```

## Encoding

Class: `10`

Opcode: `11`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `10` register class |
| `29:28` | `opcode` | instruction opcode |
| `27:22` | `ra` | destination register |
| `21:16` | `rb` | source register for MVV |
| `15:0` | `imm16` | immediate value for MVI |

## Operation

```text
ra = imm16
```

## Effects

- Writes ra
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- All 16 immediate bits are preserved.

## Example

```asm
MVI r1, 0x1234
```
