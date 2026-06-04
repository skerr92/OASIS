# JMR

## Summary

Branches to the instruction index stored in rb.

## Syntax

```asm
JMR rb
```

## Encoding

Class: `00`

Opcode: `0111`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `reserved` | must be zero |
| `19:14` | `rb` | target register |
| `13:0` | `reserved` | must be zero |

## Operation

```text
pc = rb[7:0]
```

## Effects

- Does not write registers
- does not modify memory
- branches
- flags: none.

## Edge Cases

- Only the low 8 bits of rb are used as the target.

## Example

```asm
JMR r1
```
