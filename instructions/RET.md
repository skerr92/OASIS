# RET

## Summary

Returns to the instruction index stored in r58.

## Syntax

```asm
RET
```

## Encoding

Class: `00`

Opcode: `0110`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:14` | `reserved` | must be zero |
| `13:6` | `target8` | absolute target for CALL |
| `5:0` | `reserved` | must be zero |

## Operation

```text
pc = r58[7:0]
```

## Effects

- Does not write registers
- does not modify memory
- branches
- flags: none.

## Edge Cases

- Return address register is fixed to r58 by the Base-16 toolchain ABI.

## Example

```asm
RET
```
