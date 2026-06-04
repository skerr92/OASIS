# OASIS Toolchain Plan

The toolchain should grow in layers. The assembler is the first completed layer.

## Current State

Available now:

- OASIS Base-16 assembler: `bin/oasis-asm`
- Program image generator: `bin/oasis-program-image`
- Machine-readable ISA metadata: `toolchain/generated/oasis-base16t-v0.1-draft.json`
- Opcode, register, encoding, and programming tables in `tables/`

Not available yet:

- Object file format
- Linker
- C runtime
- GCC backend
- C++ runtime or standard library support

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

### 3. Runtime Skeleton

Status: scaffolded.

Add:

- Startup sequence
- Zeroing or copying data sections, once sections exist
- Exit trap or halt convention
- Minimal headers for freestanding C

### 4. Object And Linker Format

Status: not started.

For GCC/binutils, the practical path is ELF:

- Target: `oasis16-elf`
- Bare-metal triple: `oasis16-unknown-elf`
- Sections: `.text`, `.rodata`, `.data`, `.bss`, `.stack`
- Linker script for Base-16 memory

### 5. Binutils Port

Status: not started.

GCC normally expects target binutils:

- BFD architecture
- Opcode table
- GAS assembler or adapter
- LD emulation/linker script
- objdump/readelf support

The existing OASIS assembler can guide GAS encoding, but GCC still needs object
and linker support for normal C/C++ workflows.

### 6. GCC 14 Backend

Status: scaffolded.

Initial goal:

- Darwin-hosted cross compiler
- Target `oasis16-unknown-elf`
- GCC 14 source tree
- Base-16T instruction patterns
- Language: C first
- C++ only after libgcc/runtime basics are stable

### 7. C++ Support

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
