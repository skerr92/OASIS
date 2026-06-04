# NOP

## Summary

Performs no operation.

## Syntax

```asm
NOP
```

## Encoding

Class: `01`

Opcode: `1111`

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
no operation
```

## Effects

- Does not write registers
- does not modify memory
- does not branch
- flags: none.

## Edge Cases

- Only pc advances
- reserved bits must be zero.

## Example

```asm
NOP
```
