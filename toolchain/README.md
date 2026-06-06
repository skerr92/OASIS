# OASIS Toolchain

This directory captures the path toward compiling C and C++ for OASIS cores.
The first compiler target is a freestanding GCC 14 cross toolchain for
`oasis16-unknown-elf`.

## Current Status

The Base-16 assembler is implemented in `tools/oasis_asm.py`, and OASIS v0.1
now has a working initial GCC 14/binutils toolchain path for
`oasis16-unknown-elf`.

The repository contains backend files, config integration helpers, build
wrappers, runtime files, ELF-to-image conversion, packaging scripts, and
installed-toolchain smoke tests. GitHub Actions builds the Linux toolchain
against upstream GCC/binutils source trees on release-producing refs and uploads
a Linux toolchain installer plus a source/compliance package.

Darwin arm64 toolchain artifacts are built locally on Apple Silicon hardware for
each release. The current toolchain build is not treated as reliable on
GitHub-hosted macOS runners, so Darwin archives should be attached manually to
the release after local validation.

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

This creates `toolchain/generated/oasis-base16t-v0.2-draft.json` from the source
tables in `tables/`. Compiler backends, assemblers, emulators, and compliance
harnesses should prefer generated metadata over hand-copying opcode constants.
The metadata also includes the recommended programming access-port register map.

## v0.2 Toolchain Work

1. Expand GCC lowering for wider integer modes and more complex addressing.
2. Add deeper libgcc/runtime support beyond the initial 16-bit helper set.
3. Decide the C++ freestanding policy: static initialization, exceptions, RTTI,
   allocation, and library subset.
4. Add more compiler-generated compliance and torture-style smoke tests.
5. Keep release artifacts reproducible across Linux and Darwin hosts.

The Base-16T ABI now records the first freestanding C and C++ runtime contract:
the C data model, stack-frame rules, init/fini range symbols, local static guard
hooks, heap policy, and external-memory linker symbols. See
[toolchain/abi/base16-baremetal-abi.md](abi/base16-baremetal-abi.md) and
[docs/external-memory-control.md](../docs/external-memory-control.md).

OASIS-32 toolchain work is draft planning only for now. The future Base-32T
target is documented in [spec/oasis32/abi.md](../spec/oasis32/abi.md) and
[toolchain/abi/base32-baremetal-abi.md](abi/base32-baremetal-abi.md), with
initial machine-readable opcode and encoding tables under `tables/oasis32/`.
The active build scripts still target `oasis16-unknown-elf`.

## GCC 14 Build Scripts

## Fetching Upstream Source Trees

The OASIS backend files are staged into normal upstream GCC and binutils source
trees. The CI build currently uses GCC `14.3.0` and binutils `2.46.0`.

Fetch and unpack both source archives into a local build area:

```sh
mkdir -p .build/sources

curl --fail --location --show-error \
  https://ftp.gnu.org/gnu/gcc/gcc-14.3.0/gcc-14.3.0.tar.xz \
  -o .build/sources/gcc-14.3.0.tar.xz

curl --fail --location --show-error \
  https://ftp.gnu.org/gnu/binutils/binutils-2.46.0.tar.xz \
  -o .build/sources/binutils-2.46.0.tar.xz

tar -C .build/sources -xf .build/sources/gcc-14.3.0.tar.xz
tar -C .build/sources -xf .build/sources/binutils-2.46.0.tar.xz
```

The build scripts can then use:

```sh
--gcc-src "$PWD/.build/sources/gcc-14.3.0" \
--binutils-src "$PWD/.build/sources/binutils-2.46.0"
```

For release or CI work, keep the exact versions pinned so generated artifacts
remain reproducible. For bring-up against a newer binutils release, start by
running `toolchain/scripts/apply-gcc14-backend.py --integrate-config` against
the new source tree and expect small config or documentation patch differences.

Darwin/macOS:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

The Darwin wrapper auto-detects Homebrew prefixes for `gmp`, `mpfr`, `libmpc`,
and `isl` and passes them to GCC configure. If those dependencies are installed
somewhere else, pass them explicitly:

```sh
toolchain/scripts/build-darwin-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils \
  --with-gmp /path/to/gmp \
  --with-mpfr /path/to/mpfr \
  --with-mpc /path/to/mpc \
  --with-isl /path/to/isl
```

For release Darwin arm64 artifacts, run the Darwin build locally on Apple
Silicon with `--run-tests`, then package the prefix with
`toolchain/scripts/package-toolchain-installer.sh`. Do not rely on
GitHub-hosted macOS runners for the Darwin release archive until the build is
proven reliable there.

Linux:

```sh
toolchain/scripts/build-linux-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14 \
  --binutils-src /path/to/binutils
```

This stages the backend files, configures binutils, configures GCC stage 1, and
installs the freestanding runtime and libgcc helper archive. Use `--dry-run`
first to inspect the exact commands. Add `--run-tests` to run the freestanding
smoke suite after installation.

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

Package a built prefix as a downloadable installer:

```sh
toolchain/scripts/package-toolchain-installer.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --output oasis16-toolchain.tar.gz
```

Package the OASIS source, generated metadata, tools, backend files, runtime, and
compliance tests for non-submodule consumers:

```sh
make generate
toolchain/scripts/package-source-release.sh --output oasis-source.tar.gz
```

## LLVM Backend

`toolchain/llvm/` is reserved for a future LLVM backend. The active compiler
bring-up path is GCC/binutils first.
