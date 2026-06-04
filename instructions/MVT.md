# MVT

## Summary

Stores ra into data memory.

## Syntax

```asm
MVT ra, [addr9]
```

## Encoding

Class: `11`

Opcode: `10`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `11` memory class |
| `29:28` | `opcode` | instruction opcode |
| `27:22` | `ra/addr9` | register for MVF/MVT or address high field for MSI |
| `21:13` | `addr9` | data-memory word address for MVF/MVT |
| `15:0` | `imm16` | immediate value for MSI |

## Operation

```text
memory[addr9] = ra
```

## Effects

- Does not write registers
- writes memory
- does not branch
- flags: none.

## Edge Cases

- Address is a 9-bit word index
- reserved bits must be zero.

## Example

```asm
MVI r1, 0x1234
MVT r1, [0x001]
```
