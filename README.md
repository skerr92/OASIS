# OASIS

OASIS is the Open Architecture Simplified Instruction Set: a small,
implementation-friendly ISA intended for learning, FPGA soft cores,
microcontrollers, and custom chip experiments.

This repository answers: "What must any correct OASIS CPU do?" Implementation
repositories, such as DungV, consume this contract and report compatibility
against a pinned OASIS version.

## Current Profile

OASIS v0.1 defines two profiles:

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

OASIS v0.1 is the first functional architecture and toolchain baseline. The
v0.2 work stream is now focused on a more capable core profile, deeper compiler
lowering, richer runtime support, and stronger release/compliance packaging.

OASIS v0.2-draft also starts the OASIS-32 planning scaffold. OASIS-32 is
experimental architecture groundwork for future 32-bit profiles and does not
modify OASIS v0.1 Base-16/Base-16T compatibility.

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

OASIS-32 draft planning starts at
[spec/oasis-v0.2-draft.md](spec/oasis-v0.2-draft.md) and
[docs/roadmap-32.md](docs/roadmap-32.md).

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

GitHub Actions publishes two downloadable artifacts on `main`, version tags, and
manual workflow runs:

- `oasis16-toolchain-installer`: a prebuilt OASIS Base-16T GCC/binutils prefix
  packaged with an `install.sh`
- `oasis-source-compliance-package`: the OASIS spec, tables, tools, compliance
  tests, runtime files, and backend sources for implementations that do not want
  to consume this repository as a submodule

## Development Rule

OASIS v0.1 requires:

- Complete generated instruction docs for every opcode
- Machine-readable opcode, encoding, register, target, and programming tables
- Compliance coverage for every mnemonic in the opcode table

OASIS v0.2 proposals should keep v0.1 compatibility explicit and include
matching table, documentation, assembler, compliance, and toolchain updates.
