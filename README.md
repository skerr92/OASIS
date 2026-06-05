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
| `toolchain/` | GCC/binutils backend files, runtime pieces, and build scripts |
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

`bin/oasis-cc` and `bin/oasis-c++` forward to an installed OASIS toolchain when
`OASIS_TOOLCHAIN_PREFIX` points at a prefix containing `oasis16-elf-gcc` or
`oasis16-elf-g++`. See [toolchain/README.md](toolchain/README.md) for build and
validation commands.

## Development Rule

OASIS v0.1 now requires:

- Complete generated instruction docs for every opcode
- Machine-readable opcode, encoding, register, target, and programming tables
- Compliance coverage for every mnemonic in the opcode table

Do not grow the ISA beyond Base-16/Base-16T until implementation repositories can
run and report the shared compliance tests.
