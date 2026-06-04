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

## gas/configure.tgt

```sh
oasis16-*-elf*) fmt=elf ;;
```

## ld/configure.tgt

```sh
oasis16-*-elf*) targ_emul=oasis16elf ;;
```
