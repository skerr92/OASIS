#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  build-linux-gcc14.sh --prefix PREFIX --gcc-src GCC_SRC --binutils-src BINUTILS_SRC [options]

Linux wrapper for the OASIS GCC 14 cross-toolchain build.
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

if [ "$(uname -s)" != "Linux" ]; then
  echo "error: this script is for Linux hosts" >&2
  exit 1
fi

if command -v apt-get >/dev/null 2>&1; then
  echo "Debian/Ubuntu packages: build-essential gcc-14 g++-14 make texinfo flex bison libgmp-dev libmpfr-dev libmpc-dev libisl-dev"
elif command -v dnf >/dev/null 2>&1; then
  echo "Fedora packages: gcc gcc-c++ make texinfo flex bison gmp-devel mpfr-devel libmpc-devel isl-devel"
elif command -v pacman >/dev/null 2>&1; then
  echo "Arch packages: base-devel gcc make texinfo flex bison gmp mpfr libmpc isl"
else
  echo "warning: unknown Linux package manager; ensure GCC/binutils prerequisites are installed" >&2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$SCRIPT_DIR/build-gcc14-common.sh" "$@"
