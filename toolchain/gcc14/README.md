# GCC 14 Backend Plan

The long-term goal is a GCC 14 cross compiler for OASIS Base-16T cores.

## Host Priority

1. Darwin/macOS host
2. Generic Unix-like host

## Target

Use an ELF bare-metal target for GCC/binutils work:

```text
oasis16-unknown-elf
```

Tool names should use the shorter alias:

```text
oasis16-elf-gcc
oasis16-elf-as
oasis16-elf-ld
oasis16-elf-objdump
```

## Why ELF Instead Of `none`

The existing repository metadata uses `oasis16-unknown-none` to describe the
bare-metal ISA environment. GCC and binutils are easier to build around an ELF
target because object files, sections, relocations, and linking are already
standardized.

Recommended mapping:

- ISA/runtime environment: `oasis16-unknown-none`
- GCC/binutils object target: `oasis16-unknown-elf`

## GCC Backend Coverage

- `gcc/config/oasis16/` target files
- Register classes for `r0` through `r63`
- Machine modes for 16-bit data and 32-bit instructions
- Instruction patterns for Base-16T operations
- Prologue and epilogue generation
- Calling convention implementation
- Libgcc support routines
- Driver and target config entries

Backend files live under `toolchain/gcc14/backend/`.

## Binutils Coverage

GCC expects target binutils for normal operation. Backend files live under
`toolchain/binutils/backend/` and cover:

- BFD architecture definition
- Opcode definitions
- GAS assembler support or an adapter around `oasis-asm`
- LD emulation and linker script
- objdump support

## Darwin Build Shape

Build the current freestanding GCC/binutils toolchain with:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

Supported language front ends:

```text
C and C++, freestanding, no hosted libc, targeting Base-16T
```

The C++ front end is available for freestanding experiments. The runtime now
documents and installs initial init-array, guard-variable, pure-virtual, and
heapless allocation hooks. Exceptions, RTTI, hosted libstdc++, threads, and OS
syscalls remain outside the OASIS-16 v0.2 baseline.

## v1.0 Memory And MMIO Pointers

Base-16T v1.0 pointers encode `{mmio, addr15}`. The GCC backend continues to
lower register-indirect accesses through `LDR` and `STR`; the pointer's high bit
selects MMIO. Runtime headers provide `OASIS16_MEM_PTR(type, word)` and
`OASIS16_MMIO_PTR(type, word)` so C/C++ source preserves the address-space
choice explicitly. `r59`/`sap` and `r60`/`sdata` remain fixed compiler registers
for far/staged transfer sequences.
