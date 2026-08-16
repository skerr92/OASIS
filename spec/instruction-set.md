# Instruction Set

The OASIS v1.0 instruction set is intentionally small and forms the new
compatibility baseline.

## Groups

| Group | Instructions |
| ----- | ------------ |
| Toolchain | `ADI`, `SBI`, `LDR`, `STR`, `CALL`, `RET`, `JMR`, `JLT`, `JGE`, `JLTU`, `JGEU`, `MCP` |
| ALU | `ADD`, `SUB`, `AND`, `OOR`, `XOR`, `SHR`, `SHL`, `RTR`, `RTL`, `NOT`, `MLT` |
| Branch | `JEQ`, `JNE`, `JMP`, `NOP` |
| Register | `MVV`, `MVI` |
| Memory | `MVF`, `MVT`, `MSI` with explicit `mem:` or `io:` space |

The toolchain group belongs to the Base-16T profile. Base-16T is Base-16 plus
the instructions required for freestanding C and C++ compiler support.

OASIS-32 draft instructions are planned separately under
[oasis-v0.2-draft.md](oasis-v0.2-draft.md) and `tables/oasis32/`. They carry
forward v1.0's explicit memory/MMIO distinction without sharing Base-16 binary
encodings.

See [../docs/instruction-expansion.md](../docs/instruction-expansion.md) for
v0.2 notes on optional peripheral and implementation extension templates.

See [../instructions/README.md](../instructions/README.md) for the detailed
per-instruction reference and [../tables/opcode-map.csv](../tables/opcode-map.csv)
for the machine-readable opcode map.
