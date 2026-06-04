# ABI

OASIS Base-16 defines no final application binary interface. OASIS Base-16T adds
the instructions needed for the bare-metal ABI draft to become implementable.

There is currently no standard calling convention, stack pointer, return
address register, argument register set, callee-saved register set, or object
file format.

Future ABI work should happen after the base ISA and compliance tests are stable.
The working draft for compiler work lives in
[../toolchain/abi/base16-baremetal-abi.md](../toolchain/abi/base16-baremetal-abi.md).

## C And C++ Requirements

A C/C++ toolchain needs these ABI decisions before it can be complete:

- Stack pointer register
- Return address register or return sequence
- Function call sequence
- Function return sequence
- Argument registers
- Return-value registers
- Caller-saved and callee-saved register sets
- Stack alignment
- Global/static data layout
- Startup entry point
- Linker memory map
- Object file format

Base-16T now defines the ISA mechanisms needed by this list: stack-capable
register-indirect memory access, add/sub immediate, call, return, jump-register,
and signed/unsigned comparison branches.

See [base16t.md](base16t.md).
