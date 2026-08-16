# Instruction Expansion

This note records extension guidance for OASIS Base-16T without fragmenting
implementation behavior. OASIS v1.0 has consumed one former exploration opcode.

## Goals

- Respect the v1.0 compatibility boundary.
- Give implementation authors a repeatable pattern for peripheral instructions.
- Preserve memory-mapped IO as the portable baseline.
- Make optional extension profiles easy to advertise, test, and ignore.

## Class `00` Expansion Space

Class `00` is reserved by Base-16 and defined by Base-16T for toolchain-facing
instructions. v1.0 Base-16T uses these class `00` opcodes:

| Opcode | Instruction |
| ------ | ----------- |
| `0001` | `ADI` |
| `0010` | `SBI` |
| `0011` | `LDR` |
| `0100` | `STR` |
| `0101` | `CALL` |
| `0110` | `RET` |
| `0111` | `JMR` |
| `1000` | `JLT` |
| `1001` | `JGE` |
| `1010` | `JLTU` |
| `1011` | `JGEU` |
| `1100` | `MCP` |

The remaining exploration space is therefore:

| Opcode | Suggested Use |
| ------ | ------------- |
| `0000` | Escape, system, or extension-discovery prefix |
| `1101` | Peripheral block transfer or external-memory template |
| `1110` | Interrupt/debug/control template |
| `1111` | Vendor or implementation-defined escape template |

The remaining assignments are provisional. They should become architectural only after
tables, assembler support, binutils support, and compliance tests exist.

## Peripheral Template

Peripheral instructions should describe a logical peripheral block and register
without baking one vendor's address map into the ISA.

Suggested fields:

| Field | Purpose |
| ----- | ------- |
| `ra` | Source or destination register |
| `periph` | Peripheral block identifier |
| `reg` | Register inside the peripheral block |
| `subop` | Read, write, set bits, clear bits, or fence operation |

Example candidate mnemonics:

| Mnemonic | Shape | Purpose |
| -------- | ----- | ------- |
| `PFR` | `PFR ra, periph, reg` | Read peripheral register into `ra` |
| `PTO` | `PTO ra, periph, reg` | Write `ra` to peripheral register |
| `PSET` | `PSET ra, periph, reg` | Set masked peripheral bits |
| `PCLR` | `PCLR ra, periph, reg` | Clear masked peripheral bits |

Portable software should continue to use memory-mapped IO unless an extension
profile explicitly requires these instructions.

## Candidate Peripheral Areas

- GPIO: direction, input, output, set, clear, toggle, interrupt status.
- External memory controllers: window select, wait-state setup, burst/fence.
- Timers: counter read, compare write, interrupt enable, acknowledge.
- UART/SPI/I2C: status, data, control, clock/divider setup.
- Debug/control: halt, exit code, trace control, implementation ID.

See [external-memory-control.md](external-memory-control.md) for the current
external memory controller contract. That document keeps external memory
portable through memory-mapped control blocks and linker symbols before any
dedicated instruction extension is assigned.

## Extension Profile Rules

- Every extension needs a short profile name, such as `oasis16-periph-v0.2`.
- Extension instructions must specify their interaction with registers, memory,
  program counter, interrupts, and ordering.
- Unknown extension instructions should trap, halt with an error, or decode as
  invalid according to the implementation's conformance statement.
- Compliance tests should include positive instruction tests and invalid
  encoding tests.
- Toolchains should expose extension support through explicit flags rather than
  silently assuming peripheral instructions exist.
