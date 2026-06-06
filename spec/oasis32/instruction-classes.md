# OASIS-32 Instruction Classes

Status: experimental planning draft.

OASIS-32 uses the high 4 bits of each 64-bit instruction as the top-level class
decoder.

| Class | Name | Purpose |
| ----- | ---- | ------- |
| `0x0` | `SYSTEM` | NOP, trap, halt, system and special operations |
| `0x1` | `ALU` | Register-register integer ALU |
| `0x2` | `ALUI` | Register-immediate integer ALU |
| `0x3` | `SHIFT` | Shifts, rotates, and bit manipulation |
| `0x4` | `LOAD` | Byte, halfword, and word loads |
| `0x5` | `STORE` | Byte, halfword, and word stores |
| `0x6` | `BRANCH` | Conditional PC-relative branches |
| `0x7` | `JUMP` | Jumps, calls, returns, and indirect control flow |
| `0x8` | `COMPARE` | Compare and set operations |
| `0x9` | `MOVE` | Move, constant, and immediate construction |
| `0xA` | `MULDIV` | Multiply, divide, and remainder |
| `0xB` | `ATOMIC` | Atomics and memory ordering |
| `0xC` | `CUSTOM` | Vendor/custom extension namespace |
| `0xD` | `VECTOR` | Reserved vector/SIMD namespace |
| `0xE` | `PRIVILEGED` | Reserved privileged/system namespace |
| `0xF` | `EXTENDED` | Escape and future expansion namespace |

Reserved classes and opcodes must decode as illegal instructions unless an
implementation explicitly advertises the corresponding extension.
