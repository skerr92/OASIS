# OASIS v0.2 Draft

Status: active OASIS-16 release draft.

OASIS v0.2 is the first official release target for OASIS-16. It keeps the
frozen OASIS v0.1 instruction meanings intact while promoting the current
Base-16/Base-16T work into a stable versioned contract for implementations,
toolchains, and compliance packages.

The v0.2 planning work has two tracks:

- Stabilize OASIS-16 Base-16/Base-16T for practical compiler use.
- Keep OASIS-32 draft material organized for v0.3 and later without changing
  the OASIS-16 release baseline.

OASIS-32 is not required for v0.2 implementation work. It is documented here as
groundwork for v0.3 and later.

## Draft Profiles

| Profile | Status | Purpose |
| ------- | ------ | ------- |
| `Base-16` | frozen v0.1 baseline | Compact learning and FPGA profile |
| `Base-16T` | active v0.2 release target | 16-bit compiler/toolchain profile |
| `Base-32` | experimental draft | 32-bit general-purpose integer profile |
| `Base-32T` | experimental draft | 32-bit compiler/toolchain profile |

## OASIS-16 v0.2 Baseline

The OASIS-16 v0.2 baseline is assembled from the current source-of-truth topic
pages and generated instruction references:

- [instruction-set.md](instruction-set.md)
- [encoding.md](encoding.md)
- [registers.md](registers.md)
- [memory-model.md](memory-model.md)
- [assembly.md](assembly.md)
- [base16t.md](base16t.md)
- [abi.md](abi.md)
- [../instructions/](../instructions/)

Key v0.2 changes and formalization work:

- Absolute data-memory operands are widened from `addr9` to `addr12`, providing
  a 4096-word baseline data-memory address space.
- Base-16T class `00` compiler-facing opcodes remain stable.
- The freestanding Base-16T C ABI is documented, including the data model,
  register roles, stack frame shape, and runtime/linker symbols.
- Initial freestanding C++ ABI hooks are documented and installed for
  compile/link smoke testing.
- External-memory-control guidance is documented with memory-mapped IO as the
  portable baseline.
- Implementation conformance reporting is documented for release claims.

The active release checklist lives in
[../docs/oasis16-v0.2-release-plan.md](../docs/oasis16-v0.2-release-plan.md).
Draft release notes live in
[../docs/oasis16-v0.2-release-notes.md](../docs/oasis16-v0.2-release-notes.md).

## OASIS-32 Document Set

The OASIS-32 planning contract is split across:

- [oasis32/overview.md](oasis32/overview.md)
- [oasis32/encoding.md](oasis32/encoding.md)
- [oasis32/registers.md](oasis32/registers.md)
- [oasis32/memory.md](oasis32/memory.md)
- [oasis32/instruction-classes.md](oasis32/instruction-classes.md)
- [oasis32/abi.md](oasis32/abi.md)
- [oasis32/extensions.md](oasis32/extensions.md)
- [oasis32/compliance.md](oasis32/compliance.md)

Machine-readable draft tables live under `tables/oasis32/`.

## Compatibility Rule

No OASIS-32 draft document or table may redefine OASIS-16 Base-16/Base-16T
instruction semantics. Any shared mnemonic must either keep compatible
high-level behavior or be namespaced by profile in generated tooling.

The archived [oasis-v0.1.md](oasis-v0.1.md) page remains the v0.1 compatibility
reference. OASIS-16 v0.2 implementations should use this draft and the current
topic pages for updated `addr12`, ABI, runtime, and compliance expectations.
