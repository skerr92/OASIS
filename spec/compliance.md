# Compliance

Compliance tests define ISA-visible behavior that every compatible OASIS
implementation must match. They live in `tests/compliance/` as YAML files.

Tests name the profile they target:

- `oasis-base16-v0.1-draft`
- `oasis-base16t-v0.1-draft`

Each instruction should have at least one basic test and one edge-case test where
applicable.

| Instruction | Required coverage |
| ----------- | ----------------- |
| `ADD` | Basic addition and 16-bit wrap |
| `SUB` | Basic subtraction and underflow wrap |
| `AND` | Mixed bit mask |
| `OOR` | Mixed bit mask |
| `XOR` | Mixed bit mask |
| `SHR` | Shift by zero and nonzero amount |
| `SHL` | Shift by zero and nonzero amount |
| `RTR` | Rotate by zero, one, and larger amount |
| `RTL` | Rotate by zero, one, and larger amount |
| `NOT` | Invert all bits |
| `MLT` | Basic multiply and low-16-bit truncation |
| `JEQ` | Taken and not-taken branches |
| `JNE` | Taken and not-taken branches |
| `JMP` | Unconditional branch |
| `NOP` | No architectural state change besides `pc` |
| `MVV` | Copy source register to destination register |
| `MVI` | Load immediate into register |
| `MVF` | Load data memory into register |
| `MVT` | Store register into data memory |
| `MSI` | Store immediate into data memory |

## YAML Format

```yaml
name: add_basic
profile: oasis-base16-v0.1-draft
program:
  - MVI r1, 10
  - MVI r2, 20
  - ADD r1, r2
expect:
  registers:
    r1: 30
```

## Harness Requirements

The harness should support:

- Loading an instruction memory image
- Running a program for a bounded number of instructions or cycles
- Reading selected registers, memory locations, and `pc`
- Reporting failures in a machine-readable format

Implementation repositories may translate these YAML tests into their local
assembler, simulator, emulator, or hardware verification flow.
