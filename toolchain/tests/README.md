# OASIS Toolchain Validation Tests

This directory contains assembly fixtures plus freestanding C and C++ smoke tests for the first
`oasis16-unknown-elf` GCC/binutils toolchain.

The suite is intentionally small and layered:

- `asm/oasis16p.s` verifies exact native GAS bytes, all seven P-profile
  disassemblies, and rejection of malformed reserved encodings by objdump.
- `return_constant.c`, `add.c`, and `sub.c` exercise basic HImode codegen.
- `if_else.c`, `while_loop.c`, and `for_loop.c` exercise branches.
- `call.c` exercises the `CALL`/`RET` ABI.
- `pointer_load_store.c`, `global_data.c`, and `array_access.c` exercise stack,
  pointer, and data-section flows.
- `large_global_data.c` keeps a global object above the old 512-word v0.1 data
  range so linker and ELF-image flows continue covering the v0.2 memory map.
- `cxx/guard_static.cpp` exercises explicit C++ guard helper references.
- `cxx/heapless_new.cpp` exercises the weak heapless `operator new` runtime
  hook. It is a link smoke test, not a hosted heap guarantee.

Run after installing a toolchain prefix:

```sh
toolchain/scripts/validate-installed-toolchain.sh --prefix .toolchain/oasis16
```

Use `--dry-run` to inspect commands without requiring installed tools.
