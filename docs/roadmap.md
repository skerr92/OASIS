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
- OASIS-32 draft table validation is wired into `make check` without changing
  Base-16/Base-16T semantics.

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

OASIS v0.2 is the first formal OASIS-16 release target. It should promote the
working Base-16/Base-16T architecture from experimental bring-up to a stable
versioned contract.

The active release checklist lives in
[oasis16-v0.2-release-plan.md](oasis16-v0.2-release-plan.md).

- Finalize Base-16/Base-16T v0.2 profile names and release notes.
- Keep `addr12` data-memory addressing as the v0.2 Base-16 memory baseline.
- Keep Base-16T class `00` compiler-facing opcodes stable.
- Extend compliance tests before accepting any additional architectural feature.
- Expand installed-toolchain smoke coverage for larger data-memory addresses,
  ABI stack frames, C++ runtime hooks, and runtime/linker symbols.
- Formalize the freestanding C/C++ ABI surface: data model, stack frames,
  init-array hooks, guard helpers, heapless `new`/`delete`, and exception/RTTI
  defaults.
- Publish implementation-facing conformance and external-memory-control notes.
- Keep OASIS-32 in draft planning only until OASIS-16 v0.2 is released.

## Deferred

Defer hosted libc, threads, operating-system ABIs, dynamic linking, and full
libstdc++ until the v0.2 freestanding core/toolchain path is stable.
