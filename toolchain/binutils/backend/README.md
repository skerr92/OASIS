# OASIS Binutils Backend

This directory contains files intended to be copied into a binutils source tree.

Target:

```text
oasis16-unknown-elf
```

This backend provides the OASIS source files and integration fragments needed
for the first `oasis16-unknown-elf` binutils build:

- BFD architecture definition
- ELF header constants
- Opcode table, encoder, decoder, and disassembler entry point
- GAS parser/encoder for the OASIS assembly syntax
- LD emulation parameters and linker script template
- Initial relocation names and BFD howto entries

Remaining bring-up work:

- Native build validation inside an upstream binutils source tree
- Exhaustive relocation relaxation and overflow tests

`toolchain/scripts/apply-gcc14-backend.py --integrate-config` copies these files
and patches common binutils config files when they exist.
