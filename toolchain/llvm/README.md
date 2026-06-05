# LLVM Backend Notes

This directory records the eventual LLVM backend path for `oasis16-unknown-none`.

The active compiler priority is GCC 14/binutils. LLVM remains useful later,
especially now that the ABI and generated toolchain metadata are stable enough to
feed another backend.

Minimum backend components:

- Target registration
- Register definitions for `r0` through `r63`
- Instruction definitions from `tables/opcode-map.csv`
- Calling convention lowering
- SelectionDAG or GlobalISel instruction selection
- Assembly parser/printer support
- MC encoding support
- Bare-metal driver integration

Useful first milestone:

Compile a tiny LLVM IR function into OASIS assembly for register-only arithmetic,
then assemble it with `tools/oasis_asm.py`.
