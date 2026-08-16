# STR

## Summary

Stores a word to memory or MMIO using a `{mmio, addr15}` pointer and signed word offset.

## Syntax

```asm
STR ra, [rb + off6]
```

## Encoding

Class: `00`

Opcode: `0100`

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
space[rb[15]][rb[14:0] + sign_extend(off6)] = ra
```

## Effects

- Does not write registers
- writes memory or MMIO
- does not branch
- flags: none.

## Edge Cases

- Offset is signed 6-bit word offset -32..31
- address wraps modulo 2^15 without changing the space bit.

## Example

```asm
STR r1, [r56 - 1]
```
