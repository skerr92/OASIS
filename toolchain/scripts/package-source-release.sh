#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  package-source-release.sh --output OUT.tar.gz [options]

Options:
  --name NAME     top-level directory name, default: oasis-v1.0.0-rc.1
  -h, --help      show this help

Creates a source package containing the OASIS ISA specification, tables,
compliance tests, assembler, toolchain backend files, build scripts, runtime
files, and validation tools. Generated metadata is included when present.
EOF
}

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
OUT=
NAME=oasis-v1.0.0-rc.1

while [ "$#" -gt 0 ]; do
  case "$1" in
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

if [ -z "$OUT" ]; then
  usage >&2
  exit 2
fi

case "$OUT" in
  /*) ;;
  *) OUT="$PWD/$OUT" ;;
esac

TMPDIR_ROOT=${TMPDIR:-/tmp}
STAGE=$(mktemp -d "$TMPDIR_ROOT/oasis-source.XXXXXX")
cleanup() {
  rm -rf "$STAGE"
}
trap cleanup EXIT INT TERM

mkdir -p "$STAGE/$NAME"

tar -C "$ROOT" \
  --exclude .git \
  --exclude .github \
  --exclude .build \
  --exclude .toolchain \
  --exclude .pytest_cache \
  --exclude toolchain/generated/.gitkeep \
  -cf - . | tar -C "$STAGE/$NAME" -xf -

cat > "$STAGE/$NAME/PACKAGE.md" <<'EOF'
# OASIS v1.0.0-rc.1 Source Package

This archive contains the OASIS v1.0.0-rc.1 ISA source of truth, compliance tests,
assembler, GCC/binutils backend files, runtime files, and build scripts.

Run the repository checks with:

```sh
make check
```

Build a local toolchain by downloading GCC/binutils source trees and running:

```sh
toolchain/scripts/build-linux-gcc14.sh \
  --prefix "$PWD/.toolchain/oasis16" \
  --gcc-src /path/to/gcc-14.3.0 \
  --binutils-src /path/to/binutils-2.46.0 \
  --force
```
EOF

mkdir -p "$(dirname "$OUT")"
tar -C "$STAGE" -czf "$OUT" "$NAME"
echo "created $OUT"
