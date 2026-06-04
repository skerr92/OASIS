# Instruction Set

The OASIS v0.1 instruction set is intentionally small. It should be frozen and
tested before new operations are added.

## Groups

| Group | Instructions |
| ----- | ------------ |
| ALU | `ADD`, `SUB`, `AND`, `OOR`, `XOR`, `SHR`, `SHL`, `RTR`, `RTL`, `NOT`, `MLT` |
| Branch | `JEQ`, `JNE`, `JMP`, `NOP` |
| Register | `MVV`, `MVI` |
| Memory | `MVF`, `MVT`, `MSI` |

See [../instructions/README.md](../instructions/README.md) for the detailed
per-instruction reference and [../tables/opcode-map.csv](../tables/opcode-map.csv)
for the machine-readable opcode map.
