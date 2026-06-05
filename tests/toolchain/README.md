# Toolchain Tests

These tests describe the compiler milestones. The executable smoke-test suite
lives in `toolchain/tests/c/` and is run by
`toolchain/scripts/validate-installed-toolchain.sh` once an OASIS GCC/binutils
prefix exists.

## First C Smoke Test

Source:

```c
unsigned add(unsigned a, unsigned b) {
    return a + b;
}
```

Expected compiler command:

```sh
oasis16-elf-gcc -ffreestanding -nostdlib -S examples/c/add.c -o add.s
```

Expected generated assembly shape:

```asm
; arguments in r4, r5
MVV r1, r4
ADD r1, r5
; return in r1
```

This intentionally avoids stack, memory, calls, and runtime dependencies.

## First Linked Program

After object and linker support exists:

```sh
oasis16-elf-gcc -ffreestanding -nostdlib examples/c/add.c -o add.elf
```

Then:

```sh
bin/oasis-elf2img add.elf -o add.dap16
```

The converter emits the same `dap16` and `spi16-hex` programming formats as the
assembly image flow.

## Installed Toolchain Suite

```sh
toolchain/scripts/validate-installed-toolchain.sh --prefix .toolchain/oasis16
```

Use `--dry-run` before the toolchain exists to inspect the compile, assemble,
link, objdump, and ELF-to-image stages.
