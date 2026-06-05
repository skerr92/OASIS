# Roadmap

## v0.1 Complete: Stabilize OASIS Base-16

- Architectural state is defined.
- Instruction encoding is defined.
- Memory behavior is defined.
- Reset behavior is defined.
- Current opcodes are defined.
- Reserved bits and invalid encodings are documented.
- Machine-readable opcode tables are published.

## v0.1 Complete: Make The Spec Executable

- YAML compliance tests cover every instruction.
- A dependency-free assembler is available at `bin/oasis-asm`.
- Instruction docs are generated from opcode tables.
- Opcode, register, instruction-doc, compliance, GCC, and binutils validators run
  through `make check`.
- A Python reference emulator remains useful future work.

## v0.1 Complete: Support Implementations

- Compliance tests are packaged with the source release artifact.
- Repo-to-repo dependency options are documented.
- Source package artifacts are available for users who do not want submodules.
- Conformance badges and implementation guides remain useful v0.2 support work.

## v0.1 Complete: C And C++ Toolchain Baseline

- Base-16T ABI and toolchain profile are defined.
- Bare-metal runtime files and linker scripts are present.
- GCC 14 and binutils backend files are present.
- Darwin, Linux, and generic build wrappers are present.
- Installed-toolchain validation tests are present.
- Native GCC 14/binutils build validation is wired into GitHub Actions for
  release artifact generation.
- Downloadable toolchain installer artifacts are produced on `main`, version
  tags, and manual workflow runs.

## v0.2: Fuller Core And Toolchain

- Decide the next core profile additions: byte addressing, expanded memory
  model, interrupts/exceptions, status/compare behavior, or wider program
  counters.
- Extend compliance tests before accepting each new architectural feature.
- Grow GCC lowering beyond the first 16-bit freestanding subset, including more
  robust 32-bit and 64-bit helper paths.
- Add runtime support for startup variants, static initialization, and a clearer
  halt/exit/debug convention.
- Evaluate C++ freestanding support: constructors, destructors, `new`/`delete`,
  unwind policy, RTTI policy, and a tiny standard-library subset.
- Add implementation-facing release notes and compliance report templates.

## Deferred

Defer hosted libc, threads, operating-system ABIs, dynamic linking, and full
libstdc++ until the v0.2 freestanding core/toolchain path is stable.
