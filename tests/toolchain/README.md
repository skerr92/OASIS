# Toolchain Tests

These tests describe the compiler milestones. They are not executable until the
OASIS GCC/binutils backend exists.

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
oasis16-elf-objcopy -O binary add.elf add.bin
```

A later tool should convert `add.elf` or `add.bin` into an OASIS program image.
