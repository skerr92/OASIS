# OASIS Base-16T Bare-Metal ABI Draft

Status: draft ABI used by the current GCC/binutils bring-up.

This ABI records the decisions needed to make C and C++ compilation possible for
the Base-16T toolchain profile.

## Target Names

| Purpose | Name |
| ------- | ---- |
| ISA profile | `oasis-base16t-v0.1-draft` |
| Generic bare-metal target | `oasis16-unknown-elf` |
| GCC/binutils target alias | `oasis16-elf` |

## Register Roles

| Registers | Role | Volatility |
| --------- | ---- | ---------- |
| `r0` | General register, not hardwired zero | Caller-saved |
| `r1` - `r3` | Return values and scratch | Caller-saved |
| `r4` - `r11` | Function arguments | Caller-saved |
| `r12` - `r31` | Temporaries | Caller-saved |
| `r32` - `r55` | Saved registers | Callee-saved |
| `r56` | Stack pointer `sp` | Callee-saved |
| `r57` | Frame pointer `fp` | Callee-saved |
| `r58` | Return address `ra` | Caller-saved |
| `r59` - `r63` | Reserved for toolchain, debug, or platform | Reserved |

## Calling Convention

- Arguments are passed in `r4` through `r11`.
- Additional arguments are passed on the stack.
- Return values are passed in `r1` and `r2`.
- `CALL` stores the return address in `r58`.
- `RET` returns to `r58[7:0]`.
- Stack grows down.
- Stack alignment is 2 bytes.

## Required ISA Mechanisms

Base-16T defines the instructions required by this ABI:

| Need | Base-16T mechanism |
| ---- | ------------------ |
| Stack adjustment | `ADI`, `SBI` |
| Stack-relative load/store | `LDR`, `STR` with base register `r56` |
| Function call | `CALL target8` |
| Function return | `RET` |
| Indirect branch | `JMR rb` |
| Signed comparisons | `JLT`, `JGE` |
| Unsigned comparisons | `JLTU`, `JGEU` |

The first GCC backend should target Base-16T, not Base-16.

## Memory Map

| Region | Addressing | Purpose |
| ------ | ---------- | ------- |
| Instruction memory | 8-bit instruction index | Program text |
| Data memory low words | 9-bit word index | Globals, static data, MMIO |
| Data memory high words | 9-bit word index | Stack |

The default linker script uses a 256-instruction text memory and 512-word data
memory. Implementations may override the memory map while keeping ABI register
roles stable.

## Function Example

```asm
; unsigned add(unsigned a, unsigned b)
; a in r4, b in r5, return in r1
MVV r1, r4
ADD r1, r5
RET
```
