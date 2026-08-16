# MSI

## Summary

Stores a 16-bit immediate to explicit ordinary memory or MMIO.

## Syntax

```asm
MSI space:[addr11], imm16
```

## Encoding

Class: `11`

Opcode: `11`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `11` memory class |
| `29:28` | `opcode` | instruction opcode |
| `27` | `mmio` | space selector for MSI |
| `26:16` | `addr11` | word address for MSI |
| `15:0` | `imm16` | immediate value for MSI |

## Operation

```text
space[mmio][addr11] = imm16
```

## Effects

- Does not write registers
- writes memory or MMIO
- does not branch
- flags: none.

## Edge Cases

- Space must be mem or io
- address is an 11-bit word index
- reserved bits must be zero.

## Example

```asm
MSI mem:[0x001], 0x1234
```
