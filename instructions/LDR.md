# LDR

## Summary

Loads a data-memory word using a base register and signed word offset.

## Syntax

```asm
LDR ra, [rb + off6]
```

## Encoding

Class: `00`

Opcode: `0011`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | load/store data register |
| `19:14` | `rb` | base address register |
| `13:8` | `off6` | signed word offset |
| `7:0` | `reserved` | must be zero |

## Operation

```text
ra = memory[rb + sign_extend(off6)]
```

## Effects

- Writes ra
- reads memory
- does not branch
- flags: none.

## Edge Cases

- Offset is signed 6-bit word offset -32..31
- effective address wraps modulo 2^16 before implementation address truncation.

## Example

```asm
LDR r1, [r56 + 0]
```
