# JGE

## Summary

Signed greater-than-or-equal branch.

## Syntax

```asm
JGE ra, rb, target8
```

## Encoding

Class: `00`

Opcode: `1001`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `ra` | left comparison register |
| `19:14` | `rb` | right comparison register |
| `13:6` | `target8` | absolute 8-bit instruction target |
| `5:0` | `reserved` | must be zero |

## Operation

```text
if signed(ra) >= signed(rb) then pc = target8
```

## Effects

- Does not write registers
- does not modify memory
- may branch
- flags: none.

## Edge Cases

- Target is an 8-bit instruction index
- reserved bits must be zero.

## Example

```asm
JGE r1, r2, ge
```
