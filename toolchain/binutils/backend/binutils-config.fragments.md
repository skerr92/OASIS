# Binutils Configure Fragments

These fragments show where the OASIS target must be wired into binutils. They
are the same integration points patched by
`toolchain/scripts/apply-gcc14-backend.py --integrate-config` when the files
exist in a GCC/binutils source tree.

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

For release tarballs, also patch generated `bfd/bfd-in2.h` with
`bfd_arch_oasis16`.

## bfd/reloc.c

Add:

```c
BFD_RELOC_OASIS16_16
BFD_RELOC_OASIS16_ADDR12
BFD_RELOC_OASIS16_MSI_ADDR12
BFD_RELOC_OASIS16_TARGET8
BFD_RELOC_OASIS16_CALL8
```

For release tarballs, also patch generated `bfd/bfd-in2.h` with the same BFD
relocation enum names.

## bfd/targets.c

```c
extern const bfd_target oasis16_elf32_vec;
```

Add `&oasis16_elf32_vec` to `_bfd_target_vector`.

## bfd/Makefile.am And bfd/Makefile.in

```make
ALL_MACHINES += cpu-oasis16.lo
BFD32_BACKENDS += elf32-oasis16.lo
```

## opcodes/configure

```sh
oasis16-*-elf*) ta=oasis16 ;;
```

## opcodes/disassemble.c

```c
extern int print_insn_oasis16 (bfd_vma, disassemble_info *);
```

Add `bfd_arch_oasis16` to the architecture switch and return
`print_insn_oasis16`.

## opcodes/Makefile.am And opcodes/Makefile.in

```make
TARGET32_LIBOPCODES_CFILES += oasis16-opc.c
```

## gas/configure.tgt

```sh
oasis16-*-elf*) fmt=elf ;;
```

Copy:

- `gas/config/tc-oasis16.c`
- `gas/config/tc-oasis16.h`

## ld/configure.tgt

```sh
oasis16-*-elf*) targ_emul=oasis16elf ;;
```

Copy:

- `ld/emulparams/oasis16elf.sh`
- `ld/scripttempl/oasis16.sc`
