# Memory Model

OASIS Base-16 defines separate instruction and data memory spaces.

| Memory | Addressing | Width | v0.2 size |
| ------ | ---------- | ----- | --------- |
| Instruction memory | Instruction index | 32-bit instruction | 256 instructions |
| Data memory | Word index | 16-bit word | 4096 words |

Data memory is word-addressed in Base-16. Byte ordering is not architecturally
visible because the base profile only defines whole-word accesses.

The program counter stores an 8-bit instruction index. Jump targets are absolute
8-bit instruction indexes.

Reset sets `pc = 0`. Register and memory reset values are implementation-defined
unless a future profile states otherwise.

## Programmability

Instruction memory may be initialized through synthesis, simulation files, ROM,
flash, SPI, JTAG, or another implementation-defined loader. Portable OASIS
software is represented as an ordered list of 32-bit instruction words starting
at instruction index `0x00` unless a loader specifies a different start address.

See [programming.md](programming.md) for the recommended programming model.

## External Memory

Base-16T implementations may attach external memory behind data-memory windows
or memory-mapped control blocks. External memory is not required by Base-16T,
and portable software must not assume it exists unless the platform linker map
or conformance statement advertises it.

The v0.2 external memory control expectations are documented in
[../docs/external-memory-control.md](../docs/external-memory-control.md).
