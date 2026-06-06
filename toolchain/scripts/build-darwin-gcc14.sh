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

prepend_path() {
  if [ -d "$1" ]; then
    PATH="$1:$PATH"
  fi
}

append_flag() {
  var_name=$1
  flag=$2
  eval "current=\${$var_name:-}"
  if [ -n "$current" ]; then
    eval "$var_name=\"\$current \$flag\""
  else
    eval "$var_name=\"\$flag\""
  fi
}

append_pkg_config_path() {
  if [ -d "$1" ]; then
    if [ -n "${PKG_CONFIG_PATH:-}" ]; then
      PKG_CONFIG_PATH="$1:$PKG_CONFIG_PATH"
    else
      PKG_CONFIG_PATH="$1"
    fi
  fi
}

add_homebrew_prefix() {
  formula=$1
  prefix=$("$BREW" --prefix "$formula" 2>/dev/null || true)
  if [ -z "$prefix" ]; then
    echo "warning: Homebrew package not found: $formula" >&2
    return
  fi

  append_flag CPPFLAGS "-I$prefix/include"
  append_flag LDFLAGS "-L$prefix/lib"
  append_pkg_config_path "$prefix/lib/pkgconfig"
  prepend_path "$prefix/bin"

  case "$formula" in
    gmp) OASIS_GMP_PREFIX=$prefix ;;
    mpfr) OASIS_MPFR_PREFIX=$prefix ;;
    libmpc) OASIS_MPC_PREFIX=$prefix ;;
    isl) OASIS_ISL_PREFIX=$prefix ;;
  esac
}

BREW=${BREW:-}
if [ -z "$BREW" ] && command -v brew >/dev/null 2>&1; then
  BREW=$(command -v brew)
fi
if [ -z "$BREW" ] && [ -x /opt/homebrew/bin/brew ]; then
  BREW=/opt/homebrew/bin/brew
fi
if [ -z "$BREW" ] && [ -x /usr/local/bin/brew ]; then
  BREW=/usr/local/bin/brew
fi

if [ -n "$BREW" ]; then
  prepend_path "$(dirname "$BREW")"
  echo "Homebrew detected. Expected packages: gcc@14 gmp mpfr libmpc isl texinfo flex bison"
  add_homebrew_prefix gmp
  add_homebrew_prefix mpfr
  add_homebrew_prefix libmpc
  add_homebrew_prefix isl
  add_homebrew_prefix texinfo
  add_homebrew_prefix flex
  add_homebrew_prefix bison
else
  echo "warning: Homebrew not found; ensure GCC/binutils prerequisites are installed" >&2
fi

export PATH
export CPPFLAGS="${CPPFLAGS:-}"
export LDFLAGS="${LDFLAGS:-}"
export PKG_CONFIG_PATH="${PKG_CONFIG_PATH:-}"
export OASIS_GMP_PREFIX="${OASIS_GMP_PREFIX:-}"
export OASIS_MPFR_PREFIX="${OASIS_MPFR_PREFIX:-}"
export OASIS_MPC_PREFIX="${OASIS_MPC_PREFIX:-}"
export OASIS_ISL_PREFIX="${OASIS_ISL_PREFIX:-}"

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$SCRIPT_DIR/build-gcc14-common.sh" "$@"
