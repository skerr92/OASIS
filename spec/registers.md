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

See [../tables/registers.csv](../tables/registers.csv) for the machine-readable
register table.

Base-16T's ABI draft assigns toolchain roles to some registers. See
[../toolchain/abi/base16-baremetal-abi.md](../toolchain/abi/base16-baremetal-abi.md).
