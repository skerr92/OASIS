# OASIS Runtime

This directory is reserved for the bare-metal runtime needed by C and C++.

Open decisions:

- Stack pointer register
- Return address register
- Function call and return instructions or sequences
- Argument and return-value registers
- Callee-saved and caller-saved registers
- Startup code
- Linker memory layout
- C library subset
- C++ static initialization support

Until these are defined, C/C++ support should be treated as infrastructure work,
not a complete toolchain.

## First Runtime Milestone

The first useful runtime should support a freestanding C program with:

- A reset/start symbol
- Zeroed `.bss`, once object files and sections exist
- A fixed stack region
- A halt/exit loop
- No syscalls
- No heap

Target this before C++.
