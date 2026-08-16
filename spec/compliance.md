# Compliance

Compliance tests define ISA-visible behavior that every compatible OASIS
implementation must match. They live in `tests/compliance/` as YAML files.

Tests name the profile they target:

- `oasis-base16-v0.1-draft`
- `oasis-base16t-v0.1-draft`
- `oasis-base16-v0.2-draft`
- `oasis-base16t-v0.2-draft`
- `oasis-base16-v1.0`
- `oasis-base16t-v1.0`

Each instruction should have at least one basic test and one edge-case test where
applicable.

`tools/validate_compliance_tests.py` checks that every mnemonic in
`tables/opcode-map.csv` appears in at least one compliance program.

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
| `MVF` | Load explicitly selected memory or MMIO into register |
| `MVT` | Store register into explicitly selected memory or MMIO |
| `MSI` | Store immediate into explicitly selected memory or MMIO |
| `MCP` | Copy ordinary scratch memory to a register-addressed memory/MMIO destination |

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

v0.2 tests may also describe runtime completion through the recommended
programming access port:

```yaml
expect:
  registers:
    r1: 0x002a
  pc: __oasis_exit
  exit:
    kind: normal
    symbol: __oasis_exit
    code_register: r1
    code: 0x002a
    observe:
      pc: CORE_PC
      register_selector: GPR_ADDR
      register_data: GPR_RDATA
```

`expect.exit` is a harness-facing contract. A simulator or debugger should
observe `symbol` through `CORE_PC`, select `code_register` through `GPR_ADDR`,
and compare `GPR_RDATA` with `code`. `kind: normal` uses `__oasis_exit`;
`kind: abort` uses `__oasis_abort`.

Base-16T v0.2 compliance may also include ABI-oriented fixtures. These tests
are still ISA-visible programs, but they target toolchain conventions such as
stack growth, nested-call return-address saves, callee-saved register restore,
and runtime exit/debug observation.

Runtime/linker symbol fixtures may include `expect.symbols`. Symbol
expectations are checked by compliance tooling for shape and by the installed
toolchain validation flow for actual ELF/linker availability. Valid symbol
kinds are `runtime` for startup symbols and `linker` for symbols exported by the
default linker script.

## OASIS-16P Behavioral Model

`tools/oasis16p_model.py` is the executable reference for the optional system
block. `tools/test_oasis16p_model.py` checks reset privilege, software-trap
entry, `TVAL`, `ERET`, interrupt masking and priority, `WFI` wake behavior, CSR
operations, privilege violations, illegal encodings, and MMIO fault capture.

The model owns only architectural system state. A conforming core or RTL harness
still owns general registers, instruction retirement, memory/MMIO completion,
and the precise faulting/next-PC inputs described in `exceptions.md`.

## Harness Requirements

The harness should support:

- Loading an instruction memory image
- Running a program for a bounded number of instructions or cycles
- Reading selected registers, memory locations, and `pc`
- Detecting `expect.exit` by using `CORE_PC`, `GPR_ADDR`, and `GPR_RDATA`
- Reporting `expect.symbols` coverage when the implementation uses linked ELF
  images or an equivalent runtime symbol map
- Reporting failures in a machine-readable format

Implementation repositories may translate these YAML tests into their local
assembler, simulator, emulator, or hardware verification flow.

See [../docs/conformance.md](../docs/conformance.md) for profile claim guidance.
