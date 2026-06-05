# OASIS GCC 14 Backend

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

This backend establishes:

- Target hooks for arguments, return values, addressing, LRA selection, and
  return-in-memory decisions
- Register numbering
- Register classes
- Basic 16-bit arithmetic, memory, branch, call, prologue, and epilogue patterns
- Assembly output mnemonics matching OASIS Base-16T
- Configuration snippets for `config.gcc`
- Libgcc target helper files under `../libgcc`

Remaining bring-up work:

- Real reload/LRA pressure tuning from compiler test results
- Stack argument load/store edge cases beyond the first ABI pass
- C library integration and C++ constructor/destructor support

Use `toolchain/scripts/apply-gcc14-backend.py` to copy these files into a GCC
source tree and pass `--integrate-config` to patch common GCC/libgcc config
files when they exist.
