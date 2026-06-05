# OASIS Toolchain

This directory captures the path toward compiling C and C++ for OASIS cores.
The first compiler target is a freestanding GCC 14 cross toolchain for
`oasis16-unknown-elf`.

## Current Status

The Base-16 assembler is implemented in `tools/oasis_asm.py`.

The repository now contains the OASIS backend files, config integration helper,
build wrappers, runtime files, ELF-to-image conversion, and installed-toolchain
smoke tests. What remains is the native bring-up loop: apply these files to real
GCC 14 and binutils source trees, build them, and fix any upstream API or
machine-description diagnostics that appear.

## Target Triple

ISA/runtime environment:

```text
oasis16-unknown-none
```

Meaning:

- `oasis16`: OASIS Base-16 ISA profile
- `unknown`: no vendor
- `none`: bare-metal environment

GCC/binutils object target:

```text
oasis16-unknown-elf
```

Tool aliases:

```text
oasis16-elf-gcc
oasis16-elf-g++
oasis16-elf-as
oasis16-elf-ld
oasis-elf2img
```

## Generated Metadata

Run:

```sh
make generate
```

This creates `toolchain/generated/oasis-base16t-v0.1-draft.json` from the source
tables in `tables/`. Compiler backends, assemblers, emulators, and compliance
harnesses should prefer generated metadata over hand-copying opcode constants.
The metadata also includes the recommended programming access-port register map.

## Remaining Bring-Up Work

1. Run the build scripts against real GCC 14 and binutils source trees.
2. Fix native compile diagnostics in BFD, GAS, LD, opcodes, GCC, and libgcc.
3. Run `toolchain/scripts/validate-installed-toolchain.sh` on the installed
   prefix.
4. Use validation results to tune GCC reload/LRA behavior, stack arguments, and
   machine-description coverage.
5. Add C++ only after the freestanding C toolchain is stable.

## GCC 14 Build Scripts

Darwin/macOS:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

Linux:

```sh
toolchain/scripts/build-linux-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

This stages the backend files, configures binutils, configures GCC stage 1, and
installs the draft runtime files. Use `--dry-run` first to inspect the exact
commands. Add `--run-tests` to run the freestanding C smoke suite after
installation.

Backend files:

- `toolchain/gcc14/backend/`
- `toolchain/binutils/backend/`

Stage them into source trees with:

```sh
toolchain/scripts/apply-gcc14-backend.py \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils \
  --integrate-config
```

Once an ELF exists, convert it to a core programming image with:

```sh
bin/oasis-elf2img hello.elf -o hello.dap16
bin/oasis-elf2img hello.elf --format spi16-hex -o hello.spi16
```

Installed toolchains can be validated directly:

```sh
toolchain/scripts/validate-installed-toolchain.sh --prefix "$PWD/.toolchain/oasis16"
```

## LLVM Backend

`toolchain/llvm/` is reserved for a future LLVM backend. The active compiler
bring-up path is GCC/binutils first.
