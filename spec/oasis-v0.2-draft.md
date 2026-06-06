# OASIS v0.2 Draft

Status: experimental planning draft.

OASIS v0.2 is the planning space for architecture work after the frozen OASIS
v0.1 Base-16 and Base-16T profiles. This draft does not change OASIS v0.1
compatibility, opcode meanings, compliance tests, or toolchain expectations.

The v0.2 planning work has two tracks:

- Continue stabilizing Base-16T for practical 16-bit compiler use.
- Define the OASIS-32 architecture contract early enough that future assembler,
  emulator, RTL, and compiler work can share the same source of truth.

OASIS-32 is not required for v0.2 implementation work. It is documented here as
groundwork for v0.3 and later.

## Draft Profiles

| Profile | Status | Purpose |
| ------- | ------ | ------- |
| `Base-16` | frozen v0.1 baseline | Compact learning and FPGA profile |
| `Base-16T` | active v0.2 stabilization | 16-bit compiler/toolchain profile |
| `Base-32` | experimental draft | 32-bit general-purpose integer profile |
| `Base-32T` | experimental draft | 32-bit compiler/toolchain profile |

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

No OASIS-32 draft document or table may redefine OASIS v0.1 Base-16/Base-16T
instruction semantics. Any shared mnemonic must either keep compatible
high-level behavior or be namespaced by profile in generated tooling.
