# OASIS Toolchain

This directory captures the path toward compiling C and C++ for OASIS cores.
The first compiler target is a Darwin-hosted GCC 14 cross toolchain.

## Current Status

The Base-16 assembler is implemented in `tools/oasis_asm.py`.

C and C++ compilation is not implemented yet. OASIS v0.1 still needs ABI,
runtime, object, linker, binutils, and GCC backend work before a complete C/C++
target is useful.

## Target Triple

ISA/runtime environment:

```text
oasis16-unknown-none
```

Meaning:

- `oasis16`: OASIS Base-16 ISA profile
- `unknown`: no vendor
- `none`: bare-metal environment

GCC/binutils object target:

```text
oasis16-unknown-elf
```

Tool aliases:

```text
oasis16-elf-gcc
oasis16-elf-g++
oasis16-elf-as
oasis16-elf-ld
```

## Generated Metadata

Run:

```sh
make generate
```

This creates `toolchain/generated/oasis-base16t-v0.1-draft.json` from the source
tables in `tables/`. Compiler backends, assemblers, emulators, and compliance
harnesses should prefer generated metadata over hand-copying opcode constants.
The metadata also includes the recommended programming access-port register map.

## Recommended Path

1. Freeze the Base-16 ISA and compliance tests.
2. Define the ABI in `spec/abi.md`.
3. Define a minimal runtime in `toolchain/runtime/`.
4. Add a tiny assembler-driven code generator for simple C subsets, or start an LLVM backend.
5. Add linker script/object format decisions.
6. Add compiler tests that compare generated assembly against the OASIS emulator.

## Darwin GCC 14 Start

The Darwin-hosted scaffold is:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

This validates inputs and prints the build sequence. It does not build a
compiler yet because the OASIS GCC/binutils backend skeletons are not complete.

Backend skeleton files:

- `toolchain/gcc14/backend/`
- `toolchain/binutils/backend/`

Stage them into source trees with:

```sh
toolchain/scripts/apply-gcc14-backend.py \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

## LLVM Backend Scaffold

`toolchain/llvm/` is reserved for notes and future TableGen/backend files. A real
LLVM backend will need instruction definitions, register classes, calling
convention lowering, instruction selection, and MC layer support.
