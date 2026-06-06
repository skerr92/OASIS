#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  build-darwin-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC [options]

Darwin/macOS wrapper for the OASIS GCC 14 cross-toolchain build.
Passes common options through to build-gcc14-common.sh. When Homebrew is
available, missing --with-gmp/--with-mpfr/--with-mpc/--with-isl options are
filled from brew --prefix.
EOF
}

has_option() {
  option=$1
  shift

  for arg in "$@"; do
    case "$arg" in
      "$option"|"$option"=*)
        return 0
        ;;
    esac
  done

  return 1
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
  if ! has_option --with-gmp "$@"; then
    prefix=$(brew --prefix gmp 2>/dev/null || true)
    if [ -n "$prefix" ]; then
      set -- "$@" --with-gmp "$prefix"
    fi
  fi
  if ! has_option --with-mpfr "$@"; then
    prefix=$(brew --prefix mpfr 2>/dev/null || true)
    if [ -n "$prefix" ]; then
      set -- "$@" --with-mpfr "$prefix"
    fi
  fi
  if ! has_option --with-mpc "$@"; then
    prefix=$(brew --prefix libmpc 2>/dev/null || true)
    if [ -n "$prefix" ]; then
      set -- "$@" --with-mpc "$prefix"
    fi
  fi
  if ! has_option --with-isl "$@"; then
    prefix=$(brew --prefix isl 2>/dev/null || true)
    if [ -n "$prefix" ]; then
      set -- "$@" --with-isl "$prefix"
    fi
  fi
else
  echo "warning: Homebrew not found; ensure GCC/binutils prerequisites are installed" >&2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$SCRIPT_DIR/build-gcc14-common.sh" "$@"
