# CALL

## Summary

Stores a return address in r58 and branches to an absolute target.

## Syntax

```asm
CALL target8
```

## Encoding

Class: `00`

Opcode: `0101`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:14` | `reserved` | must be zero |
| `13:6` | `target8` | absolute target for CALL |
| `5:0` | `reserved` | must be zero |

## Operation

```text
r58 = pc + 1; pc = target8
```

## Effects

- Writes r58
- does not modify memory
- branches
- flags: none.

## Edge Cases

- Target is an 8-bit instruction index
- nested calls must save r58 when needed.

## Example

```asm
CALL function
```
