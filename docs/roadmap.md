# Roadmap

## Phase 1: Stabilize OASIS Base-16

- Architectural state is defined.
- Instruction encoding is defined.
- Memory behavior is defined.
- Reset behavior is defined.
- Current opcodes are defined.
- Reserved bits and invalid encodings are documented.
- Machine-readable opcode tables are published.

## Phase 2: Make The Spec Executable

- YAML compliance tests cover every instruction.
- A dependency-free assembler is available at `bin/oasis-asm`.
- Instruction docs are generated from opcode tables.
- Opcode, register, instruction-doc, compliance, GCC, and binutils validators run
  through `make check`.
- A Python reference emulator remains useful future work.

## Phase 3: Support Implementations

- Provide compliance reports
- Document repo-to-repo dependency options
- Add a conformance badge such as `OASIS Base-16 Compliant`
- Add guides for building a minimal OASIS core

## Phase 4: C And C++ Toolchain

- Base-16T ABI and toolchain profile are defined.
- Bare-metal runtime files and linker scripts are present.
- GCC 14 and binutils backend files are present.
- Darwin, Linux, and generic build wrappers are present.
- Installed-toolchain validation tests are present.
- Remaining work is native build validation against upstream GCC 14 and binutils
  source trees.

## Deferred

Defer privilege modes, interrupts, exceptions, byte addressing, new ALU features,
and hosted C/C++ support until Base-16/Base-16T freestanding C bring-up is
validated in real toolchain builds.
