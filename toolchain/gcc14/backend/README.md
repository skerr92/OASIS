# OASIS GCC 14 Backend Skeleton

This directory contains source files intended to be copied into a GCC 14 source
tree.

Target:

```text
oasis16-unknown-elf
```

Install location inside GCC:

```text
gcc/config/oasis16/
```

This is an initial backend skeleton, not a complete GCC port. It establishes:

- Target hook stubs
- Register numbering
- Register classes
- Basic 16-bit arithmetic instruction patterns
- Assembly output mnemonics matching OASIS Base-16T
- Configuration snippets for `config.gcc`

Known missing pieces:

- Real prologue/epilogue generation
- Reload/LRA tuning
- Addressing-mode constraints
- Function call lowering
- Libgcc integration
- Full machine description coverage
- Target-specific tests

Use `toolchain/scripts/apply-gcc14-backend.py` to copy these files into a GCC
source tree.
