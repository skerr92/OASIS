# MVV

## Summary

Copies rb into ra.

## Syntax

```asm
MVV ra, rb
```

## Encoding

Class: `10`

Opcode: `10`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `10` register class |
| `29:28` | `opcode` | instruction opcode |
| `27:22` | `ra` | destination register |
| `21:16` | `rb` | source register for MVV |
| `15:0` | `imm16` | immediate value for MVI |

## Operation

```text
ra = rb
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
MVI r1, 0x1234
MVV r2, r1
```
