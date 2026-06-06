#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  package-toolchain-installer.sh --prefix PREFIX --output OUT.tar.gz [options]

Options:
  --name NAME     top-level directory name in the archive, default: oasis16-toolchain
  -h, --help      show this help

Creates a relocatable installer archive for an installed OASIS toolchain prefix.
The archive includes install.sh, README.md, and the toolchain payload.
EOF
}

PREFIX=
OUT=
NAME=oasis16-toolchain

while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix)
      PREFIX=$2
      shift 2
      ;;
    --output)
      OUT=$2
      shift 2
      ;;
    --name)
      NAME=$2
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

if [ -z "$PREFIX" ] || [ -z "$OUT" ]; then
  usage >&2
  exit 2
fi

case "$PREFIX" in
  /*) ;;
  *) PREFIX="$PWD/$PREFIX" ;;
esac

case "$OUT" in
  /*) ;;
  *) OUT="$PWD/$OUT" ;;
esac

if [ ! -d "$PREFIX" ]; then
  echo "error: prefix not found: $PREFIX" >&2
  exit 1
fi

if [ ! -x "$PREFIX/bin/oasis16-elf-gcc" ]; then
  echo "error: missing expected compiler: $PREFIX/bin/oasis16-elf-gcc" >&2
  exit 1
fi

TMPDIR_ROOT=${TMPDIR:-/tmp}
STAGE=$(mktemp -d "$TMPDIR_ROOT/oasis-toolchain.XXXXXX")
cleanup() {
  rm -rf "$STAGE"
}
trap cleanup EXIT INT TERM

mkdir -p "$STAGE/$NAME"
tar -C "$PREFIX" -cf - . | tar -C "$STAGE/$NAME" -xf -

cat > "$STAGE/$NAME/README.md" <<'EOF'
# OASIS Base-16T Toolchain

This archive contains a prebuilt `oasis16-unknown-elf` GCC/binutils toolchain
for OASIS Base-16T v0.2.

Install into a prefix with:

```sh
./install.sh /path/to/oasis16
```

Then add the toolchain to your environment:

```sh
export OASIS_TOOLCHAIN_PREFIX=/path/to/oasis16
export PATH="$OASIS_TOOLCHAIN_PREFIX/bin:$PATH"
```
EOF

cat > "$STAGE/$NAME/install.sh" <<'EOF'
#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: ./install.sh PREFIX" >&2
  exit 2
fi

DEST=$1
mkdir -p "$DEST"
tar -C "$(dirname "$0")" \
  --exclude ./install.sh \
  --exclude ./README.md \
  -cf - . | tar -C "$DEST" -xf -

echo "installed OASIS toolchain to $DEST"
echo "export OASIS_TOOLCHAIN_PREFIX=$DEST"
echo "export PATH=\$OASIS_TOOLCHAIN_PREFIX/bin:\$PATH"
EOF
chmod +x "$STAGE/$NAME/install.sh"

mkdir -p "$(dirname "$OUT")"
tar -C "$STAGE" -czf "$OUT" "$NAME"
echo "created $OUT"
