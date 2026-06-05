# OASIS Toolchain Validation Tests

This directory contains freestanding C smoke tests for the first
`oasis16-unknown-elf` GCC/binutils toolchain.

The suite is intentionally small and layered:

- `return_constant.c`, `add.c`, and `sub.c` exercise basic HImode codegen.
- `if_else.c`, `while_loop.c`, and `for_loop.c` exercise branches.
- `call.c` exercises the `CALL`/`RET` ABI.
- `pointer_load_store.c`, `global_data.c`, and `array_access.c` exercise stack,
  pointer, and data-section flows.

Run after installing a toolchain prefix:

```sh
toolchain/scripts/validate-installed-toolchain.sh --prefix .toolchain/oasis16
```

Use `--dry-run` to inspect commands without requiring installed tools.
