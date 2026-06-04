#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  build-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC

Generic Unix-like scaffold for building an OASIS GCC 14 cross toolchain.
This does not build yet because the OASIS binutils and GCC backend skeletons are
not complete.
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

echo "OASIS generic GCC 14 toolchain scaffold"
echo "prefix:       $PREFIX"
echo "gcc-src:      $GCC_SRC"
echo "binutils-src: $BINUTILS_SRC"
echo
echo "Target: oasis16-unknown-elf"
echo "Alias:  oasis16-elf"
echo
echo "Backend skeleton files exist under toolchain/gcc14/backend and toolchain/binutils/backend."
echo "Use toolchain/scripts/apply-gcc14-backend.py to copy them into source trees."
echo
echo "Not building yet: the backend skeleton is not complete enough for GCC/binutils."
exit 1
