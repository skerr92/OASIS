# OASIS-32 Compliance Planning

Status: experimental planning draft.

OASIS-32 compliance is not active yet. This document records the expected shape
of future compliance work.

## Compliance Inputs

Future OASIS-32 compliance should be generated from:

- `tables/oasis32/opcode-map.csv`
- `tables/oasis32/encoding-formats.csv`
- `tables/oasis32/registers.csv`
- `tables/oasis32/extensions.csv`
- per-instruction documentation under `instructions/oasis32/`

## Planned Test Areas

| Area | Examples |
| ---- | -------- |
| ALU | `ADD`, `SUB`, logical ops, `NEG`, `NOT` |
| Immediates | `ADDI`, logical immediates, `MVI` |
| Memory | byte, halfword, word loads/stores and alignment |
| Branches | signed and unsigned branch conditions |
| Calls | `CALL`, `RET`, indirect jumps |
| ABI | argument passing, return values, stack alignment |
| Illegal instructions | reserved class/op decode behavior |

## Emulator First

Before RTL compliance begins, OASIS-32 should have a reference emulator capable
of decoding instruction words, executing the base profile, and reporting
register, memory, and PC state for tests.
