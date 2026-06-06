# OASIS-32 Overview

Status: experimental planning draft.

OASIS-32 is a proposed 32-bit profile family for OASIS. It is intended to keep
the OASIS preference for simple decode, explicit instruction classes, clear
documentation, and implementation-friendly hardware.

OASIS-32 is not an RTL target yet. The immediate goal is to define an
architecture contract before implementation work begins.

## Profile Goals

OASIS-32 should provide:

- 32-bit general-purpose registers
- 32-bit arithmetic and logical operations
- 32-bit byte-addressed memory
- fixed-width 64-bit instruction encoding
- explicit load/store sizes
- flagless branches and comparisons
- enough immediate width for compiler-friendly code generation
- reserved extension space for privileged, atomic, vector, and custom features

## Planned Profiles

| Profile | Role |
| ------- | ---- |
| `Base-32` | Core 32-bit integer ISA |
| `Base-32T` | Compiler/toolchain-oriented profile |
| `OASIS-32M` | Multiply/divide extension |
| `OASIS-32A` | Atomic and memory-ordering extension |
| `OASIS-32P` | Privileged/system extension |
| `OASIS-32V` | Vector/SIMD extension |
| `OASIS-32C` | Custom/vendor extension namespace |

## Non-Goals For This Scaffold

- No RTL implementation is defined here.
- No assembler or emulator implementation is required yet.
- No OASIS v0.1 Base-16/Base-16T semantics are changed.
- No privileged exception model is finalized.
