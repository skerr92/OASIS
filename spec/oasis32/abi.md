# OASIS Base-32T Bare-Metal ABI Draft

Status: experimental planning draft.

This ABI records early decisions needed for future C and C++ toolchain work on
OASIS-32. It is not implemented by the current OASIS v1.0 toolchain.

The companion toolchain-facing ABI note is
[../../toolchain/abi/base32-baremetal-abi.md](../../toolchain/abi/base32-baremetal-abi.md).

## Target Names

| Purpose | Draft Name |
| ------- | ---------- |
| ISA profile | `oasis-base32t-v0.3-draft` |
| Generic bare-metal target | `oasis32-unknown-elf` |
| GCC/binutils target alias | `oasis32-elf` |

## C Data Model

| C type | Size | Alignment |
| ------ | ---- | --------- |
| `char` | 8 bits | 1 byte |
| `short` | 16 bits | 2 bytes |
| `int` | 32 bits | 4 bytes |
| `long` | 32 bits | 4 bytes |
| `long long` | 64 bits | 4 bytes, compiler-emulated initially |
| pointer | 32 bits | 4 bytes |

The initial data model is ILP32.

## Register Roles

| Registers | Role | Volatility |
| --------- | ---- | ---------- |
| `r0` / `zero` | constant zero | immutable |
| `r1` / `ra` | return address | caller-saved |
| `r2` / `sp` | stack pointer | callee-saved |
| `r3` / `fp` | frame pointer | callee-saved |
| `r4` - `r5` / `rv0` - `rv1` | return values | caller-saved |
| `r6` - `r15` / `a0` - `a9` | arguments | caller-saved |
| `r16` - `r31` / `t0` - `t15` | temporaries | caller-saved |
| `r32` - `r47` / `s0` - `s15` | saved registers | callee-saved |
| `r48` - `r63` | platform/reserved | reserved |

## Calling Convention

- Arguments are passed in `a0` through `a9`.
- Additional arguments are passed on the stack.
- Return values are passed in `rv0` and `rv1`.
- `CALL` writes the return address to `ra`.
- `RET` returns to `ra`.
- Stack grows down.
- Stack pointer must be 4-byte aligned at public call boundaries.
- Frame pointer use is optional unless required for debugging or dynamic stack
  allocation.

## Required Base-32T Mechanisms

| Need | Mechanism |
| ---- | --------- |
| Stack adjustment | `ADDI`, `SUBI` or `ADDI` with negative immediate |
| Stack-relative load/store | `LDW`, `STW`, byte/halfword forms |
| Function call | `CALL pc_rel32` |
| Function return | `RET` |
| Indirect call/jump | `JALR`, `JMR` |
| Signed comparison | `BLT`, `BGE`, `SLT` |
| Unsigned comparison | `BLTU`, `BGEU`, `SLTU` |
| Constant materialization | `MVI rd, imm32` |

## Open ABI Questions

- C++ exception and RTTI policy.
- Static constructor/destructor runtime policy.
- Whether `long long` must be supported by libgcc helpers in the first backend.
- Whether a platform register should be reserved for TLS or small-data access.
