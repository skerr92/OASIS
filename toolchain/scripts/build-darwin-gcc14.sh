#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  build-darwin-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC

This script is scaffolding for a Darwin-hosted OASIS GCC 14 cross toolchain.
It validates inputs and prints the intended build stages. It will not build a
compiler until the OASIS binutils and GCC backend skeletons are completed.
EOF
}

PREFIX=
GCC_SRC=
BINUTILS_SRC=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix)
      PREFIX=$2
      shift 2
      ;;
    --gcc-src)
      GCC_SRC=$2
      shift 2
      ;;
    --binutils-src)
      BINUTILS_SRC=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ "$(uname -s)" != "Darwin" ]; then
  echo "error: this script is for Darwin/macOS hosts" >&2
  exit 1
fi

if [ -z "$PREFIX" ] || [ -z "$GCC_SRC" ] || [ -z "$BINUTILS_SRC" ]; then
  usage >&2
  exit 2
fi

if [ ! -d "$GCC_SRC" ]; then
  echo "error: GCC source directory not found: $GCC_SRC" >&2
  exit 1
fi

if [ ! -d "$BINUTILS_SRC" ]; then
  echo "error: binutils source directory not found: $BINUTILS_SRC" >&2
  exit 1
fi

echo "OASIS Darwin GCC 14 toolchain scaffold"
echo "prefix:       $PREFIX"
echo "gcc-src:      $GCC_SRC"
echo "binutils-src: $BINUTILS_SRC"
echo
echo "Required host tools on macOS:"
echo "  xcode-select --install"
echo "  brew install gcc@14 gmp mpfr libmpc isl texinfo flex bison"
echo
echo "Build stages once OASIS backend ports exist:"
echo "  1. Apply or stage OASIS binutils target files."
echo "  2. Build oasis16-elf binutils."
echo "  3. Apply or stage OASIS GCC target files."
echo "  4. Build stage-1 oasis16-elf-gcc with --without-headers --enable-languages=c."
echo "  5. Add libgcc/runtime support."
echo "  6. Build C++ only after ABI/runtime support is stable."
echo
echo "Backend skeleton files exist under toolchain/gcc14/backend and toolchain/binutils/backend."
echo "Use toolchain/scripts/apply-gcc14-backend.py to copy them into source trees."
echo
echo "Not building yet: the backend skeleton is not complete enough for GCC/binutils."
exit 1
