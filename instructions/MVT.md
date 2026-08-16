# MVT

## Summary

Stores a register to explicit ordinary memory or MMIO.

## Syntax

```asm
MVT ra, space:[addr11]
```

## Encoding

Class: `11`

Opcode: `10`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `11` memory class |
| `29:28` | `opcode` | instruction opcode |
| `27:22` | `ra` | register for MVF/MVT |
| `21` | `mmio` | space selector for MVF/MVT |
| `20:10` | `addr11` | word address for MVF/MVT |
| `9:0` | `reserved` | must be zero |

## Operation

```text
space[mmio][addr11] = ra
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
MVI r1, 0x1234
MVT r1, io:[0x001]
```
