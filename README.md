# OASIS

OASIS is the Open Architecture Simplified Instruction Set: a small,
implementation-friendly ISA intended for learning, FPGA soft cores,
microcontrollers, and custom chip experiments.

This repository answers: "What must any correct OASIS CPU do?" Implementation
repositories, such as DungV, consume this contract and report compatibility
against a pinned OASIS version.

## Current Profile

OASIS v0.1-draft defines two profiles:

- Base-16: compact ISA foundation
- Base-16T: Base-16 plus toolchain operations for C/C++ compiler targets

Base-16 provides:

- 16-bit data path
- 32-bit instructions
- 64 general purpose registers
- Word-addressed data memory
- Basic ALU, move/immediate, load/store, and jump/branch operations
- No privilege modes, interrupts, exceptions, or status flags

Base-16T adds immediate arithmetic, register-indirect memory access, call/return,
jump-register, and signed/unsigned comparison branches.

Start with [spec/oasis-v0.1.md](spec/oasis-v0.1.md).

## Repository Layout

| Path | Purpose |
| ---- | ------- |
| `spec/` | Versioned ISA specification and topic pages |
| `instructions/` | Per-instruction reference pages |
| `tables/` | Machine-readable opcode and encoding tables |
| `tests/compliance/` | Shared ISA compliance test definitions |
| `tools/` | Documentation and table validation tools |
| `bin/` | User-facing tool wrappers |
| `toolchain/` | C/C++ toolchain planning and runtime scaffolding |
| `docs/` | Roadmap and process notes |

## Tools

Assemble OASIS Base-16 programs:

```sh
bin/oasis-asm examples/base16/add_store.oas -o add_store.mem
```

Generate programming scripts for SPI/JTAG bridges:

```sh
bin/oasis-program-image examples/base16/add_store.oas -o add_store.dap16
```

Run repository checks:

```sh
make check
```

C and C++ wrappers exist as explicit placeholders under `bin/`. See
[toolchain/README.md](toolchain/README.md) and
[toolchain/plan.md](toolchain/plan.md) for the Darwin-first GCC 14 path needed
before `oasis-cc` and `oasis-c++` can compile programs.

## Development Rule

Do not grow the ISA until OASIS Base-16 v0.1 has complete instruction docs,
machine-readable opcode tables, and compliance tests that implementation repos
can run.
