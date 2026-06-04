# MSI

## Summary

Stores a 16-bit immediate into data memory.

## Syntax

```asm
MSI [addr9], imm16
```

## Encoding

Class: `11`

Opcode: `11`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `11` memory class |
| `29:28` | `opcode` | instruction opcode |
| `27:22` | `ra/addr9` | register for MVF/MVT or address high field for MSI |
| `21:13` | `addr9` | data-memory word address for MVF/MVT |
| `15:0` | `imm16` | immediate value for MSI |

## Operation

```text
memory[addr9] = imm16
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
MSI [0x001], 0x1234
```
