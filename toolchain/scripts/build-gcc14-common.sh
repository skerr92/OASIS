#!/usr/bin/env sh
set -eu

TARGET=oasis16-unknown-elf
TARGET_ALIAS=oasis16-elf

usage() {
  cat <<'EOF'
Usage:
  build-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC [options]
  build-gcc14-common.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC [options]

Options:
  --jobs N       parallel make jobs, default: host CPU count when detectable
  --with-gmp DIR
                 GMP install prefix for GCC configure
  --with-mpfr DIR
                 MPFR install prefix for GCC configure
  --with-mpc DIR
                 MPC install prefix for GCC configure
  --with-isl DIR
                 ISL install prefix for GCC configure
  --clean        remove OASIS build directories before configuring
  --dry-run      print commands without executing them
  --force        overwrite staged backend files in source trees
  --run-tests    run freestanding smoke tests after installing runtime files
  -h, --help     show this help
EOF
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PREFIX=
GCC_SRC=
BINUTILS_SRC=
JOBS=
GMP_PREFIX=
MPFR_PREFIX=
MPC_PREFIX=
ISL_PREFIX=
CLEAN=0
DRY_RUN=0
FORCE=0
RUN_TESTS=0

detect_jobs() {
  if command -v sysctl >/dev/null 2>&1; then
    sysctl -n hw.ncpu 2>/dev/null && return
  fi
  if command -v nproc >/dev/null 2>&1; then
    nproc && return
  fi
  echo 1
}

quote() {
  printf "'%s'" "$(printf "%s" "$1" | sed "s/'/'\\\\''/g")"
}

run() {
  printf "+"
  for arg in "$@"; do
    printf " "
    quote "$arg"
  done
  printf "\n"

  if [ "$DRY_RUN" -eq 0 ]; then
    "$@"
  fi
}

run_in_dir() {
  dir=$1
  shift

  printf "+ cd "
  quote "$dir"
  printf " &&"
  for arg in "$@"; do
    printf " "
    quote "$arg"
  done
  printf "\n"

  if [ "$DRY_RUN" -eq 0 ]; then
    (cd "$dir" && "$@")
  fi
}

require_dir() {
  if [ ! -d "$2" ]; then
    echo "error: $1 directory not found: $2" >&2
    exit 1
  fi
}

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
    --jobs)
      JOBS=$2
      shift 2
      ;;
    --with-gmp)
      GMP_PREFIX=$2
      shift 2
      ;;
    --with-gmp=*)
      GMP_PREFIX=${1#*=}
      shift
      ;;
    --with-mpfr)
      MPFR_PREFIX=$2
      shift 2
      ;;
    --with-mpfr=*)
      MPFR_PREFIX=${1#*=}
      shift
      ;;
    --with-mpc)
      MPC_PREFIX=$2
      shift 2
      ;;
    --with-mpc=*)
      MPC_PREFIX=${1#*=}
      shift
      ;;
    --with-isl)
      ISL_PREFIX=$2
      shift 2
      ;;
    --with-isl=*)
      ISL_PREFIX=${1#*=}
      shift
      ;;
    --clean)
      CLEAN=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --run-tests)
      RUN_TESTS=1
      shift
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

if [ -z "$JOBS" ]; then
  JOBS=$(detect_jobs)
fi

require_dir GCC "$GCC_SRC"
require_dir binutils "$BINUTILS_SRC"

BUILD_ROOT="$ROOT/.build/oasis16-gcc14"
BINUTILS_BUILD="$BUILD_ROOT/binutils"
GCC_BUILD="$BUILD_ROOT/gcc"

echo "OASIS GCC 14 toolchain build"
echo "target:       $TARGET"
echo "alias:        $TARGET_ALIAS"
echo "prefix:       $PREFIX"
echo "gcc-src:      $GCC_SRC"
echo "binutils-src: $BINUTILS_SRC"
echo "jobs:         $JOBS"
echo "dry-run:      $DRY_RUN"
echo "run-tests:    $RUN_TESTS"
if [ -n "$GMP_PREFIX" ]; then
  echo "gmp-prefix:   $GMP_PREFIX"
fi
if [ -n "$MPFR_PREFIX" ]; then
  echo "mpfr-prefix:  $MPFR_PREFIX"
fi
if [ -n "$MPC_PREFIX" ]; then
  echo "mpc-prefix:   $MPC_PREFIX"
fi
if [ -n "$ISL_PREFIX" ]; then
  echo "isl-prefix:   $ISL_PREFIX"
fi
echo

if [ "$CLEAN" -eq 1 ]; then
  run rm -rf "$BUILD_ROOT"
fi

if [ "$FORCE" -eq 1 ]; then
  run python3 "$ROOT/toolchain/scripts/apply-gcc14-backend.py" \
    --gcc-src "$GCC_SRC" \
    --binutils-src "$BINUTILS_SRC" \
    --integrate-config \
    --force
else
  run python3 "$ROOT/toolchain/scripts/apply-gcc14-backend.py" \
    --gcc-src "$GCC_SRC" \
    --binutils-src "$BINUTILS_SRC" \
    --integrate-config
fi

run mkdir -p "$BINUTILS_BUILD"
run mkdir -p "$GCC_BUILD"

run_in_dir "$BINUTILS_BUILD" "$BINUTILS_SRC/configure" \
  --target="$TARGET" \
  --program-prefix="$TARGET_ALIAS-" \
  --prefix="$PREFIX" \
  --disable-nls \
  --disable-werror \
  --disable-gdb \
  --disable-sim
run make -C "$BINUTILS_BUILD" -j "$JOBS"
run make -C "$BINUTILS_BUILD" install

set -- "$GCC_SRC/configure" \
  --target="$TARGET" \
  --program-prefix="$TARGET_ALIAS-" \
  --prefix="$PREFIX" \
  --enable-languages=c,c++ \
  --without-headers \
  --with-system-zlib \
  --with-insnemit-partitions=7 \
  --disable-shared \
  --disable-threads \
  --disable-libssp \
  --disable-libstdcxx \
  --disable-nls \
  --disable-multilib
if [ -n "$GMP_PREFIX" ]; then
  set -- "$@" "--with-gmp=$GMP_PREFIX"
fi
if [ -n "$MPFR_PREFIX" ]; then
  set -- "$@" "--with-mpfr=$MPFR_PREFIX"
fi
if [ -n "$MPC_PREFIX" ]; then
  set -- "$@" "--with-mpc=$MPC_PREFIX"
fi
if [ -n "$ISL_PREFIX" ]; then
  set -- "$@" "--with-isl=$ISL_PREFIX"
fi
run_in_dir "$GCC_BUILD" "$@"
run make -C "$GCC_BUILD" all-gcc -j "$JOBS"
run make -C "$GCC_BUILD" all-target-libgcc -j "$JOBS"
run make -C "$GCC_BUILD" install-gcc
run make -C "$GCC_BUILD" install-target-libgcc

run mkdir -p "$PREFIX/$TARGET/lib"
run mkdir -p "$PREFIX/$TARGET/include"
run mkdir -p "$PREFIX/bin"
run mkdir -p "$PREFIX/tools"
run cp "$ROOT/toolchain/runtime/crt0.S" "$PREFIX/$TARGET/lib/crt0.S"
run cp "$ROOT/toolchain/runtime/crt0.oas" "$PREFIX/$TARGET/lib/crt0.oas"
run cp "$ROOT/toolchain/runtime/cxxabi.c" "$PREFIX/$TARGET/lib/cxxabi.c"
run cp "$ROOT/toolchain/runtime/cxxnew.cpp" "$PREFIX/$TARGET/lib/cxxnew.cpp"
run cp "$ROOT/toolchain/runtime/linker/oasis16.ld" "$PREFIX/$TARGET/lib/oasis16.ld"
run cp "$ROOT/toolchain/runtime/include/oasis.h" "$PREFIX/$TARGET/include/oasis.h"
run cp "$ROOT/bin/oasis-elf2img" "$PREFIX/bin/oasis-elf2img"
run cp "$ROOT/bin/oasis-program-image" "$PREFIX/bin/oasis-program-image"
run cp "$ROOT/bin/oasis-asm" "$PREFIX/bin/oasis-asm"
run cp "$ROOT/tools/oasis_elf2img.py" "$PREFIX/tools/oasis_elf2img.py"
run cp "$ROOT/tools/oasis_program_image.py" "$PREFIX/tools/oasis_program_image.py"
run cp "$ROOT/tools/oasis_asm.py" "$PREFIX/tools/oasis_asm.py"

if [ "$RUN_TESTS" -eq 1 ]; then
  run "$ROOT/toolchain/scripts/validate-installed-toolchain.sh" --prefix "$PREFIX"
fi

echo
echo "Build stages completed."
