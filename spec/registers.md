# Registers

OASIS Base-16 defines 64 general purpose registers named `r0` through `r63`.

| Property | Value |
| -------- | ----- |
| Register width | 16 bits |
| Register address width | 6 bits |
| Register count | 64 |
| `r0` behavior | Writable |

There are no architectural status flags. Arithmetic wrap, carry, zero,
negative, overflow, and comparison results are not recorded in a flags register.

Base-16 and Base-16T do not define a hardwired zero register. All 64 registers
are architecturally writable, including `r0`.

Base-16T assigns ABI roles and assembler/toolchain aliases to selected
registers for C and C++ code generation. These aliases are software names only:
hardware still observes the architectural `r0` through `r63` register numbers.

See [../tables/registers.csv](../tables/registers.csv) for the machine-readable
register table.

See [../toolchain/abi/base16-baremetal-abi.md](../toolchain/abi/base16-baremetal-abi.md)
for the Base-16T calling convention and register-role assignments.

The OASIS-32 draft explores wider registers and may define different register
behavior in a separate profile. Those draft choices do not change Base-16 or
Base-16T.
