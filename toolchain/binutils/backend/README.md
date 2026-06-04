# OASIS Binutils Backend Skeleton

This directory contains files intended to be copied into a binutils source tree.

Target:

```text
oasis16-unknown-elf
```

This is a scaffold, not a complete binutils port. It gives the port a concrete
shape:

- BFD architecture placeholder
- ELF header constants
- Opcode table structure
- GAS target placeholder
- LD emulation parameters and linker script template

Known missing pieces:

- Relocation definitions and handling
- Full GAS parser/encoder
- BFD ELF backend implementation
- LD emulation scripts wired into binutils configure
- objdump disassembler support

The existing `tools/oasis_asm.py` remains the working flat-image assembler while
this port matures.
