# MCP

## Summary

Copies one ordinary scratch word to a register-addressed memory or MMIO destination.

## Syntax

```asm
MCP [rb], mem:[scratch11]
```

## Encoding

Class: `00`

Opcode: `1100`

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `31:30` | `class` | `00` toolchain class |
| `29:26` | `opcode` | instruction opcode |
| `25:20` | `rb` | destination `{mmio, addr15}` pointer register |
| `19:9` | `scratch11` | ordinary-memory scratch source |
| `8:0` | `reserved` | must be zero |

## Operation

```text
space[rb[15]][rb[14:0]] = memory[scratch11]
```

## Effects

- Does not write registers
- reads ordinary memory
- writes memory or MMIO
- does not branch
- flags: none.

## Edge Cases

- Source must be inside the platform scratch block
- operation is not atomic with a preceding MSI
- reserved bits must be zero.

## Example

```asm
MVI sap, io:0x0100
MSI mem:[0x0000], 0x1234
MCP [sap], mem:[0x0000]
```
