# ABI

OASIS Base-16 defines no application binary interface. OASIS Base-16T adds the
instructions needed for a bare-metal ABI draft to become implementable.

The working draft for compiler work lives in
[../toolchain/abi/base16-baremetal-abi.md](../toolchain/abi/base16-baremetal-abi.md).
That document is now the register and calling-convention source for the
experimental `oasis16-unknown-elf` GCC/binutils work.

## C And C++ Requirements

A C/C++ toolchain needs these ABI decisions before it can be complete. The
Base-16T draft has assigned the first version of each item:

- Stack pointer register: `r56`
- Frame pointer register: `r57`
- Return address register: `r58`
- Function call sequence: `CALL target8`
- Function return sequence: `RET`
- Argument registers: `r4` through `r11`
- Return-value registers: `r1` and `r2`
- Caller-saved and callee-saved register sets: defined by the ABI draft
- Stack alignment: 2 bytes
- Global/static data layout: draft ELF linker map
- Startup entry point: `_start`
- Object file format: ELF32 skeleton for `oasis16-unknown-elf`

Base-16T now defines the ISA mechanisms needed by this list: stack-capable
register-indirect memory access, add/sub immediate, call, return, jump-register,
and signed/unsigned comparison branches.

See [base16t.md](base16t.md).
