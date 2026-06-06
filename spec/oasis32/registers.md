# OASIS-32 Registers

Status: experimental planning draft.

OASIS-32 instruction fields reserve 8 bits for register IDs. Base-32 initially
defines 64 architectural general-purpose registers and reserves IDs `64` through
`255` for future profiles.

## Register Model

| Register IDs | Role |
| ------------ | ---- |
| `r0` | hardwired zero, recommended for Base-32 |
| `r1` - `r63` | general-purpose registers |
| `r64` - `r255` | reserved |

Reads from `r0` return zero. Writes to `r0` are ignored in Base-32.

## ABI Aliases

The draft Base-32T ABI uses:

| Register | Alias | Role |
| -------- | ----- | ---- |
| `r0` | `zero` | constant zero |
| `r1` | `ra` | return address |
| `r2` | `sp` | stack pointer |
| `r3` | `fp` | frame pointer |
| `r4` | `rv0` | primary return value |
| `r5` | `rv1` | secondary return value |
| `r6` - `r15` | `a0` - `a9` | argument registers |
| `r16` - `r31` | `t0` - `t15` | caller-saved temporaries |
| `r32` - `r47` | `s0` - `s15` | callee-saved registers |
| `r48` - `r63` | platform/reserved | platform, debug, or extension use |

The ABI aliases are not required by hardware, but assemblers and compiler
backends should support them for Base-32T.
