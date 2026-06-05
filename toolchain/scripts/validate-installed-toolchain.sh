#!/usr/bin/env sh
set -eu

TARGET_ALIAS=oasis16-elf

usage() {
  cat <<'EOF'
Usage:
  validate-installed-toolchain.sh --prefix PREFIX [options]

Options:
  --tests DIR    C smoke-test directory, default: toolchain/tests/c
  --dry-run      print commands without executing them
  -h, --help     show this help
EOF
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
PREFIX=
TEST_DIR="$ROOT/toolchain/tests/c"
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

CC="$PREFIX/bin/$TARGET_ALIAS-gcc"
AS="$PREFIX/bin/$TARGET_ALIAS-as"
LD="$PREFIX/bin/$TARGET_ALIAS-ld"
OBJDUMP="$PREFIX/bin/$TARGET_ALIAS-objdump"
ELF2IMG="$PREFIX/bin/oasis-elf2img"
OUT_DIR="$ROOT/.build/toolchain-tests"

if [ "$DRY_RUN" -eq 0 ]; then
  for tool in "$CC" "$AS" "$LD" "$OBJDUMP" "$ELF2IMG"; do
    if [ ! -x "$tool" ]; then
      echo "error: missing executable tool: $tool" >&2
      exit 1
    fi
  done
fi

run mkdir -p "$OUT_DIR"
run "$AS" "$ROOT/toolchain/runtime/crt0.S" -o "$OUT_DIR/crt0.o"

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

echo "toolchain validation completed"
