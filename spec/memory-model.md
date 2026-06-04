# Memory Model

OASIS Base-16 defines separate instruction and data memory spaces.

| Memory | Addressing | Width | v0.1 size |
| ------ | ---------- | ----- | --------- |
| Instruction memory | Instruction index | 32-bit instruction | 256 instructions |
| Data memory | Word index | 16-bit word | 512 words |

Data memory is word-addressed in v0.1. Byte ordering is not architecturally
visible because the base profile only defines whole-word accesses.

The program counter stores an 8-bit instruction index. Jump targets are absolute
8-bit instruction indexes.

Reset sets `pc = 0`. Register and memory reset values are implementation-defined
unless a future profile states otherwise.
