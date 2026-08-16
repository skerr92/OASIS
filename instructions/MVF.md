# MVF

## Summary

Loads a word from explicit ordinary memory or MMIO.

## Syntax

```asm
MVF ra, space:[addr11]
```

## Encoding

Class: `11`

Opcode: `01`

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
ra = space[mmio][addr11]
```

## Effects

- Writes ra
- reads memory or MMIO
- does not branch
- flags: none.

## Edge Cases

- Space must be mem or io
- address is an 11-bit word index
- reserved bits must be zero.

## Example

```asm
MVF r1, mem:[0x001]
```
