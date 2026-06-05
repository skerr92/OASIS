# OASIS Toolchain Plan

The v0.1 toolchain baseline is in place. The assembler, ELF conversion,
GCC/binutils backend files, runtime pieces, build scripts, validation scripts,
and release packaging scripts are now part of the repository.

## Current State

Available now:

- OASIS Base-16 assembler: `bin/oasis-asm`
- Program image generator: `bin/oasis-program-image`
- ELF-to-program-image converter: `bin/oasis-elf2img`
- Darwin and Linux GCC 14 build wrappers
- Installed-toolchain C smoke-test runner
- Machine-readable ISA metadata: `toolchain/generated/oasis-base16t-v0.1-draft.json`
- Opcode, register, encoding, and programming tables in `tables/`

Not available yet:

- Hosted libc support
- Full C++ runtime or standard library support
- Complete 32-bit/64-bit libgcc lowering

## Toolchain Profile

OASIS Base-16T is the compiler target profile. It keeps Base-16 intact and uses
class `00` for ABI-friendly operations:

- `ADI` and `SBI` for stack adjustment and immediate arithmetic
- `LDR` and `STR` for register-indirect memory access
- `CALL`, `RET`, and `JMR` for function control flow
- `JLT`, `JGE`, `JLTU`, and `JGEU` for signed and unsigned C comparisons

GCC and binutils should target Base-16T.

## Milestones

### 1. Assembler And Program Images

Status: implemented.

- Assemble `.oas` into 32-bit instruction words.
- Generate Verilog memory files.
- Generate transport-neutral programming scripts.
- Generate SPI-friendly programming frames.

### 2. ABI Draft

Status: Base-16T draft defined.

Define:

- Stack pointer
- Return address handling
- Argument registers
- Return registers
- Caller-saved and callee-saved registers
- Stack alignment
- Program entry point
- Memory map

See `toolchain/abi/base16-baremetal-abi.md`.

### 3. Runtime

Status: implemented for freestanding C bring-up.

- Startup sequence
- Exit trap or halt convention
- Minimal headers for freestanding C
- Linker script symbols for text, data, BSS, and stack
- Libgcc helper routines for the first 16-bit arithmetic set

### 4. Object And Linker Format

Status: implemented and covered by the release build workflow.

For GCC/binutils, the practical path is ELF:

- Target: `oasis16-elf`
- Bare-metal triple: `oasis16-unknown-elf`
- Sections: `.text`, `.rodata`, `.data`, `.bss`, `.stack`
- Linker script for Base-16 memory

### 5. Binutils Port

Status: implemented and covered by the release build workflow.

- BFD architecture
- Opcode table
- GAS assembler
- LD emulation/linker script
- objdump support

The existing OASIS assembler remains useful for flat images, while GAS/BFD/LD
are the ELF path for normal GCC workflows.

### 6. GCC 14 Backend

Status: implemented for the v0.1 freestanding baseline and covered by the
release build workflow.

Initial goal:

- Darwin-hosted cross compiler
- Target `oasis16-unknown-elf`
- GCC 14 source tree
- Base-16T instruction patterns
- Languages: freestanding C plus C++ front-end bring-up
- C++ runtime features remain v0.2 work

### 7. Compiler Validation

Status: implemented.

The C smoke tests in `toolchain/tests/c/` cover return values, arithmetic,
branches, calls, pointer load/store, globals, and arrays. Run them with
`toolchain/scripts/validate-installed-toolchain.sh` after installing a toolchain
prefix.

### 8. C++ Support

Status: future.

C++ requires more runtime work:

- Constructors/destructors
- Static initialization
- Personality/unwind decision
- Minimal `new`/`delete`
- libstdc++ support or an intentionally tiny freestanding subset

## Recommended First Compiler Target

The first compiler should target a freestanding, bare-metal C subset:

- No hosted libc
- No dynamic allocation
- No exceptions
- No RTTI
- No threads
- No OS syscalls

That gets arithmetic, simple control flow, and hardware-oriented firmware in
reach before attempting a full hosted environment.
