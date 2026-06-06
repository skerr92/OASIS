# OASIS-16 v0.2 Release Plan

Status: active release planning.

OASIS-16 v0.2 is the first official release target for the 16-bit architecture.
The goal is to promote the working Base-16/Base-16T design from experimental
bring-up into a stable contract for hardware implementations, toolchains, and
compliance packages.

## Release Scope

- Base-16 and Base-16T profile definitions.
- `addr12` absolute data-memory operands and the 4096-word baseline data-memory
  address space.
- Stable Base-16T compiler-facing class `00` operations.
- Freestanding C ABI: data model, calling convention, stack frame shape, and
  linker/runtime symbols.
- Initial freestanding C++ ABI hooks: init/fini arrays, guard helpers,
  heapless `new`/`delete`, and pure-virtual abort handling.
- Init/fini range symbols are required, but automatic constructor/destructor
  execution is optional platform runtime policy for v0.2.
- Programming-image tooling for implementation bring-up.
- External-memory-control guidance with memory-mapped IO as the portable
  baseline.
- Source/compliance packaging for submodule and non-submodule consumers.

## Non-Goals

- Hosted libc or operating-system ABIs.
- Full libstdc++, threads, dynamic linking, exceptions, or RTTI as required
  baseline features.
- Required automatic `.init_array` or `.fini_array` execution in the default
  startup object.
- New required peripheral instructions.
- OASIS-32 implementation requirements.

## Formalization Checklist

- Freeze the Base-16 and Base-16T v0.2 profile names.
- Publish a versioned v0.2 spec entry that points at the current topic pages and
  generated instruction references.
- Keep generated metadata, instruction docs, and validation checks in sync with
  the v0.2 tables.
- Expand compliance output into an implementation-facing report template. The
  starting template is
  [conformance-report-template.md](conformance-report-template.md).
- Add installed-toolchain smoke coverage for ABI stack frames, C++ runtime hook
  symbols, and larger data-memory objects. The validation script now covers C
  smoke tests, explicit C++ guard-helper references, and heapless `operator new`
  linking.
- Add ABI-oriented compliance coverage. The current fixture set includes nested
  call return-address save/restore and callee-saved register preservation.
- Verify release artifact generation for the toolchain installer and
  source/compliance package. Linux and source artifacts are produced by GitHub
  Actions; Darwin arm64 toolchains are built locally for release attachment.
- Document compatibility expectations for v0.1 implementations moving to v0.2.
- Draft release notes are captured in
  [oasis16-v0.2-release-notes.md](oasis16-v0.2-release-notes.md).

## Acceptance Criteria

- `make check` passes from a clean checkout.
- Generated instruction docs and metadata match the source tables.
- The GCC/binutils backend validates against the staged backend checks.
- Installed-toolchain validation passes for the release artifact.
- Compliance fixtures cover every required Base-16/Base-16T instruction and the
  v0.2 memory-addressing behavior.
- Runtime/linker symbol expectations are covered by compliance metadata and
  installed-toolchain validation.
- Release notes clearly separate required baseline behavior from optional
  extension guidance.

## Next Objectives

1. Finalize release artifact names, checksums, and Darwin arm64 local build
   procedure.
