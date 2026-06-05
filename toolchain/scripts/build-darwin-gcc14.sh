#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  build-darwin-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC [options]

Darwin/macOS wrapper for the OASIS GCC 14 cross-toolchain build.
Passes --jobs, --clean, --dry-run, --force, and --run-tests through to
build-gcc14-common.sh.
EOF
}

if [ "$#" -gt 0 ]; then
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
  esac
fi

if [ "$(uname -s)" != "Darwin" ]; then
  echo "error: this script is for Darwin/macOS hosts" >&2
  exit 1
fi

if ! xcode-select -p >/dev/null 2>&1; then
  echo "error: Xcode command line tools are required; run xcode-select --install" >&2
  exit 1
fi

if command -v brew >/dev/null 2>&1; then
  echo "Homebrew detected. Expected packages: gcc@14 gmp mpfr libmpc isl texinfo flex bison"
else
  echo "warning: Homebrew not found; ensure GCC/binutils prerequisites are installed" >&2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$SCRIPT_DIR/build-gcc14-common.sh" "$@"
