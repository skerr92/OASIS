# Binutils Port Plan

OASIS needs a binutils port before a normal GCC toolchain is comfortable.

## Target

```text
oasis16-unknown-elf
```

## Components

- `bfd/cpu-oasis16.c`
- `bfd/elf32-oasis16.c`
- `include/elf/oasis16.h`
- `opcodes/oasis16-opc.c`
- `gas/config/tc-oasis16.c`
- `ld/emulparams/oasis16elf.sh`
- `ld/scripttempl/oasis16.sc`

## Relationship To Existing Assembler

`tools/oasis_asm.py` is useful immediately for flat program images. GAS support
will eventually replace or wrap that logic for ELF object files.

The opcode source should remain `tables/opcode-map.csv`; binutils tables should
be generated or checked against it.
