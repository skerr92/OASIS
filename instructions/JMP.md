# JMP

## Summary

Branches unconditionally to an absolute target.

## Syntax

```asm
JMP target8
```

## Encoding

Class: `01`

Opcode: `1110`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `01` ALU/jump class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | source register for conditional branches |
| `19:14` | `rb` | source register for conditional branches |
| `13:6` | `target8` | absolute 8-bit instruction target |
| `5:0` | `reserved` | must be zero |

## Operation

```text
pc = target8
```

## Effects

- Does not write registers
- does not modify memory
- branches
- flags: none.

## Edge Cases

- Target is an 8-bit instruction index
- reserved bits must be zero.

## Example

```asm
JMP start
```
