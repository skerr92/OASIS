# Binutils Configure Fragments

These fragments show where the OASIS target must be wired into binutils. They
are documentation until the backend is complete enough to compile.

## bfd/config.bfd

```sh
oasis16-*-elf*)
  targ_defvec=oasis16_elf32_vec
  targ_selvecs=
  ;;
```

## include/elf/common.h

```c
#define EM_OASIS16 0x4f16
```

Use a real assigned ELF machine value when one exists. `0x4f16` is only for
experimental bring-up.

## bfd/archures.c

```c
extern const bfd_arch_info_type bfd_oasis16_arch;
```

Add `bfd_arch_oasis16` to `enum bfd_architecture`.

## bfd/reloc.c

Add:

```c
BFD_RELOC_OASIS16_16
BFD_RELOC_OASIS16_ADDR9
BFD_RELOC_OASIS16_TARGET8
BFD_RELOC_OASIS16_CALL8
```

## gas/configure.tgt

```sh
oasis16-*-elf*) fmt=elf ;;
```

## ld/configure.tgt

```sh
oasis16-*-elf*) targ_emul=oasis16elf ;;
```

Copy:

- `ld/emulparams/oasis16elf.sh`
- `ld/scripttempl/oasis16.sc`
