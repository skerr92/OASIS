#!/usr/bin/env sh
set -eu

TARGET=oasis16-unknown-elf
TARGET_ALIAS=oasis16-elf

usage() {
  cat <<'EOF'
Usage:
  validate-installed-toolchain.sh --prefix PREFIX [options]

Options:
  --tests DIR    C smoke-test directory, default: toolchain/tests/c
  --cxx-tests DIR
                 C++ smoke-test directory, default: toolchain/tests/cxx
  --dry-run      print commands without executing them
  -h, --help     show this help
EOF
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PREFIX=
TEST_DIR="$ROOT/toolchain/tests/c"
CXX_TEST_DIR="$ROOT/toolchain/tests/cxx"
DRY_RUN=0

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

while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix)
      PREFIX=$2
      shift 2
      ;;
    --tests)
      TEST_DIR=$2
      shift 2
      ;;
    --cxx-tests)
      CXX_TEST_DIR=$2
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
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

if [ -z "$PREFIX" ]; then
  usage >&2
  exit 2
fi

if [ ! -d "$TEST_DIR" ]; then
  echo "error: test directory not found: $TEST_DIR" >&2
  exit 1
fi

if [ ! -d "$CXX_TEST_DIR" ]; then
  echo "error: C++ test directory not found: $CXX_TEST_DIR" >&2
  exit 1
fi

CC="$PREFIX/bin/$TARGET_ALIAS-gcc"
CXX="$PREFIX/bin/$TARGET_ALIAS-g++"
AS="$PREFIX/bin/$TARGET_ALIAS-as"
LD="$PREFIX/bin/$TARGET_ALIAS-ld"
OBJDUMP="$PREFIX/bin/$TARGET_ALIAS-objdump"
ELF2IMG="$PREFIX/bin/oasis-elf2img"
OUT_DIR="$ROOT/.build/toolchain-tests"

if [ "$DRY_RUN" -eq 0 ]; then
  for tool in "$CC" "$CXX" "$AS" "$LD" "$OBJDUMP" "$ELF2IMG"; do
    if [ ! -x "$tool" ]; then
      echo "error: missing executable tool: $tool" >&2
      exit 1
    fi
  done

  for helper in \
    "$PREFIX/tools/oasis_elf2img.py" \
    "$PREFIX/tools/oasis_program_image.py" \
    "$PREFIX/tools/oasis_asm.py"
  do
    if [ ! -r "$helper" ]; then
      echo "error: missing installed helper: $helper" >&2
      exit 1
    fi
  done

  for runtime_file in \
    "$PREFIX/$TARGET/lib/crt0.S" \
    "$PREFIX/$TARGET/lib/crt0.oas" \
    "$PREFIX/$TARGET/lib/cxxabi.c" \
    "$PREFIX/$TARGET/lib/cxxnew.cpp" \
    "$PREFIX/$TARGET/lib/oasis16.ld" \
    "$PREFIX/$TARGET/include/oasis.h"
  do
    if [ ! -r "$runtime_file" ]; then
      echo "error: missing installed runtime file: $runtime_file" >&2
      exit 1
    fi
  done
fi

run mkdir -p "$OUT_DIR"
run "$AS" "$ROOT/toolchain/runtime/crt0.S" -o "$OUT_DIR/crt0.o"
run "$CC" -ffreestanding -nostdlib -S "$ROOT/toolchain/runtime/cxxabi.c" -o "$OUT_DIR/cxxabi.s"
run "$AS" "$OUT_DIR/cxxabi.s" -o "$OUT_DIR/cxxabi.o"
run "$CXX" -ffreestanding -nostdlib -fno-exceptions -fno-rtti -S "$ROOT/toolchain/runtime/cxxnew.cpp" -o "$OUT_DIR/cxxnew.s"
run "$AS" "$OUT_DIR/cxxnew.s" -o "$OUT_DIR/cxxnew.o"

for source in "$TEST_DIR"/*.c; do
  name=$(basename "$source" .c)
  asm="$OUT_DIR/$name.s"
  obj="$OUT_DIR/$name.o"
  elf="$OUT_DIR/$name.elf"
  dump="$OUT_DIR/$name.dump"
  image="$OUT_DIR/$name.dap16"

  run "$CC" -ffreestanding -nostdlib -S "$source" -o "$asm"
  run "$AS" "$asm" -o "$obj"
  run "$LD" -T "$ROOT/toolchain/runtime/linker/oasis16.ld" "$OUT_DIR/crt0.o" "$obj" -o "$elf"
  run "$OBJDUMP" -d "$elf"
  if [ "$DRY_RUN" -eq 0 ]; then
    "$OBJDUMP" -d "$elf" > "$dump"
  else
    printf "+ "
    quote "$OBJDUMP"
    printf " '-d' "
    quote "$elf"
    printf " > "
    quote "$dump"
    printf "\n"
  fi
  run "$ELF2IMG" "$elf" -o "$image"
done

for source in "$CXX_TEST_DIR"/*.cpp; do
  name=$(basename "$source" .cpp)
  asm="$OUT_DIR/$name.s"
  obj="$OUT_DIR/$name.o"
  elf="$OUT_DIR/$name.elf"
  dump="$OUT_DIR/$name.dump"
  image="$OUT_DIR/$name.dap16"

  run "$CXX" -ffreestanding -nostdlib -fno-exceptions -fno-rtti -S "$source" -o "$asm"
  run "$AS" "$asm" -o "$obj"
  run "$LD" -T "$ROOT/toolchain/runtime/linker/oasis16.ld" \
    "$OUT_DIR/crt0.o" \
    "$OUT_DIR/cxxabi.o" \
    "$OUT_DIR/cxxnew.o" \
    "$obj" \
    -o "$elf"
  run "$OBJDUMP" -d "$elf"
  if [ "$DRY_RUN" -eq 0 ]; then
    "$OBJDUMP" -d "$elf" > "$dump"
  else
    printf "+ "
    quote "$OBJDUMP"
    printf " '-d' "
    quote "$elf"
    printf " > "
    quote "$dump"
    printf "\n"
  fi
  run "$ELF2IMG" "$elf" -o "$image"
done

echo "toolchain validation completed"
