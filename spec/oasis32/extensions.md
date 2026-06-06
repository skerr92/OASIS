# OASIS-32 Extensions

Status: experimental planning draft.

OASIS-32 reserves extension namespaces before implementation work begins. This
keeps the base profile small while giving future profiles stable places to grow.

## Extension Namespaces

| Extension | Purpose |
| --------- | ------- |
| `OASIS-32I` | Base integer operations |
| `OASIS-32T` | Compiler/toolchain support |
| `OASIS-32M` | Multiply, divide, and remainder |
| `OASIS-32A` | Atomics and memory ordering |
| `OASIS-32P` | Privileged/system operations |
| `OASIS-32V` | Vector/SIMD operations |
| `OASIS-32C` | Custom/vendor operations |

## Rules

- Reserved opcodes are illegal unless a profile or extension defines them.
- Custom/vendor opcodes must live in class `0xC` unless standardized.
- Experimental opcodes must be marked unstable in machine-readable tables.
- Implementations must document every non-base extension they advertise.
- Standard extensions must include compliance tests before being marked stable.

## Illegal Instruction Behavior

Base-32 implementations without a privileged trap model may halt or enter an
implementation-defined error state on illegal instruction decode.

Future privileged profiles should raise an illegal-instruction exception.
