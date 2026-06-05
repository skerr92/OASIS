# Instruction Set

The OASIS v0.1 instruction set is intentionally small. It should be frozen and
tested before new operations are added.

## Groups

| Group | Instructions |
| ----- | ------------ |
| Toolchain | `ADI`, `SBI`, `LDR`, `STR`, `CALL`, `RET`, `JMR`, `JLT`, `JGE`, `JLTU`, `JGEU` |
| ALU | `ADD`, `SUB`, `AND`, `OOR`, `XOR`, `SHR`, `SHL`, `RTR`, `RTL`, `NOT`, `MLT` |
| Branch | `JEQ`, `JNE`, `JMP`, `NOP` |
| Register | `MVV`, `MVI` |
| Memory | `MVF`, `MVT`, `MSI` |

The toolchain group belongs to the Base-16T profile. Base-16T is Base-16 plus
the instructions required for freestanding C and C++ compiler support.

See [../docs/instruction-expansion.md](../docs/instruction-expansion.md) for
v0.2 notes on optional peripheral and implementation extension templates.

See [../instructions/README.md](../instructions/README.md) for the detailed
per-instruction reference and [../tables/opcode-map.csv](../tables/opcode-map.csv)
for the machine-readable opcode map.
