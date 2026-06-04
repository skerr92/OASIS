# LLVM Backend Notes

This is a placeholder for an eventual LLVM backend targeting
`oasis16-unknown-none`.

The immediate compiler priority is a Darwin-hosted GCC 14/binutils path. LLVM
remains useful later, especially once the ABI and generated toolchain metadata
are stable.

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
