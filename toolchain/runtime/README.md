# OASIS Runtime

This directory contains the first Base-16T bare-metal runtime pieces for the
`oasis16-unknown-elf` toolchain profile.

## Files

- `crt0.S` is the ELF/GAS startup file. It defines `_start`, initializes `r56`
  as the stack pointer, calls `main`, and parks in `__oasis_exit`.
- `crt0.oas` is the same startup shape for the standalone `oasis-asm` program
  image flow.
- `linker/oasis16.ld` defines the draft 256-instruction text memory and
  512-word data memory layout.
- `include/oasis.h` exposes the runtime exit and abort hooks.
- `libgcc/oasis16-libgcc.S` provides the first 16-bit arithmetic helper
  routines used by GCC lowering.

## ABI Assumptions

- `r1` and `r2` carry return values.
- `r4` through `r11` carry incoming arguments.
- `r56` is `sp`.
- `r57` is `fp`.
- `r58` is `ra`; `CALL` writes it and `RET` consumes it.
- Stack slots are 16-bit data-memory words and the stack grows downward.

## Current Scope

The runtime anchors freestanding C experiments once GCC and binutils build
successfully. It does not provide a hosted C library, syscalls, heap allocation,
object constructors, or destructors.
