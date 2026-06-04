# Registers

OASIS Base-16 defines 64 general purpose registers named `r0` through `r63`.

| Property | Value |
| -------- | ----- |
| Register width | 16 bits |
| Register address width | 6 bits |
| Register count | 64 |
| `r0` behavior | Writable in v0.1 |

There are no architectural status flags in v0.1. Arithmetic wrap, carry, zero,
negative, overflow, and comparison results are not recorded in a flags register.

Future versions may define register aliases, a hardwired zero register, or a
calling convention.
