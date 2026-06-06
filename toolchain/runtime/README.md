# OASIS Runtime

This directory contains the first Base-16T bare-metal runtime pieces for the
`oasis16-unknown-elf` toolchain profile.

## Files

- `crt0.S` is the ELF/GAS startup file. It defines `_start`, initializes `r56`
  as the stack pointer, calls `main`, and parks in `__oasis_exit`.
- `crt0.oas` is the same startup shape for the standalone `oasis-asm` program
  image flow.
- `cxxabi.c` provides minimal freestanding C++ ABI hooks for pure virtual calls
  and local static guard variables.
- `cxxnew.cpp` provides heapless weak-default allocation behavior by parking in
  `__oasis_abort`.
- `linker/oasis16.ld` defines the Base-16T 256-instruction text memory and
  4096-word data memory layout.
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

## Exit And Abort

`main` returns its 16-bit exit code in `r1`. The startup code then parks at
`__oasis_exit`, leaving `r1` intact for a debugger, simulator, or compliance
harness to read through the programming access port.

Runtime helper failures park at `__oasis_abort`. This is abnormal termination;
the value left in `r1` is implementation-defined unless a helper documents a
more specific diagnostic value.

## Current Scope

The runtime anchors freestanding C experiments once GCC and binutils build
successfully. It does not provide a hosted C library or syscalls.

## C++ Runtime Direction

The Base-16T ABI now reserves the first freestanding C++ hooks:

- init-array and optional fini-array linker ranges
- `__cxa_pure_virtual`
- local static guard helpers
- weak `operator new` / `operator delete` hooks when a heap provider exists

The default runtime remains heapless and exception-free. C++ experiments should
assume `-fno-exceptions` and `-fno-rtti` until a fuller runtime policy is
implemented.

The runtime source files are installed into the toolchain prefix so a platform
can compile and archive them with its preferred memory policy.

## External Memory Direction

Implementations with external memory should expose linker symbols such as
`__oasis_extmem_start`, `__oasis_extmem_end`, `__oasis_heap_start`,
`__oasis_heap_end`, and `__oasis_stack_top`. The default linker script does not
place sections in external memory unless a platform-specific script overrides
the memory map.
