# OASIS Base-32T Bare-Metal Toolchain ABI Draft

Status: experimental planning draft.

This document is the toolchain-facing companion to
`spec/oasis32/abi.md`. It records expected compiler, assembler, linker, and
runtime interfaces for future OASIS-32 work. The current working toolchain
remains `oasis16-unknown-elf`.

## Target Names

| Purpose | Draft Name |
| ------- | ---------- |
| ISA profile | `oasis-base32t-v0.3-draft` |
| GCC/binutils target | `oasis32-unknown-elf` |
| Tool alias prefix | `oasis32-elf-` |

Expected tool names:

```text
oasis32-elf-gcc
oasis32-elf-g++
oasis32-elf-as
oasis32-elf-ld
oasis32-elf-objdump
```

## Data Model

Base-32T should use ILP32:

| Type | Size |
| ---- | ---- |
| `char` | 8 bits |
| `short` | 16 bits |
| `int` | 32 bits |
| `long` | 32 bits |
| `long long` | 64 bits, initially helper-backed |
| pointer | 32 bits |

## Calling Convention Summary

| ABI Role | Registers |
| -------- | --------- |
| zero | `r0` |
| return address | `r1` / `ra` |
| stack pointer | `r2` / `sp` |
| frame pointer | `r3` / `fp` |
| return values | `r4` - `r5` / `rv0` - `rv1` |
| arguments | `r6` - `r15` / `a0` - `a9` |
| caller-saved temporaries | `r16` - `r31` / `t0` - `t15` |
| callee-saved registers | `r32` - `r47` / `s0` - `s15` |
| reserved/platform | `r48` - `r63` |

Stack grows down and is 4-byte aligned at public call boundaries.

## Backend Planning Notes

Future GCC/binutils work should start from OASIS-16 lessons but should not copy
the 16-bit backend shape directly. Base-32T should lower common C operations
directly:

- 32-bit integer arithmetic in registers
- base-plus-32-bit-offset memory addressing
- byte, halfword, and word loads/stores
- PC-relative calls and branches
- register-indirect calls and jumps
- direct 32-bit constant materialization with `MVI`
- signed and unsigned compare/branch and set operations

The first backend should define relocations for:

| Relocation | Purpose |
| ---------- | ------- |
| `R_OASIS32_NONE` | no relocation |
| `R_OASIS32_32` | absolute 32-bit data |
| `R_OASIS32_PC32` | signed 32-bit PC-relative target |
| `R_OASIS32_CALL32` | call target |
| `R_OASIS32_BRANCH32` | branch target |
| `R_OASIS32_LO32` | low/full 32-bit immediate payload |

Precise relocation numbering belongs in the future binutils backend table.

## Runtime Planning Notes

The first Base-32T runtime should include:

- `crt0` that initializes `sp` and branches to `main`
- default linker script with byte-addressed text, rodata, data, bss, and stack
- freestanding exit/halt convention
- libgcc helpers for 64-bit arithmetic as needed
- optional weak hooks for board startup and debug output

C++ policy remains open for constructors, destructors, allocation, RTTI, and
exceptions.
