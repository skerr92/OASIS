#!/usr/bin/env python3
"""Copy OASIS GCC/binutils backend skeleton files into source trees."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]
GCC_BACKEND = ROOT / "toolchain" / "gcc14" / "backend" / "gcc"
LIBGCC_BACKEND = ROOT / "toolchain" / "gcc14" / "backend" / "libgcc"
BINUTILS_BACKEND = ROOT / "toolchain" / "binutils" / "backend"


def copy_tree(src: Path, dst: Path, force: bool) -> list[Path]:
    copied: list[Path] = []
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        relative = path.relative_to(src)
        target = dst / relative
        if target.exists() and not force:
            raise FileExistsError(f"{target} already exists; pass --force to overwrite")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(target)
    return copied


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gcc-src", type=Path, required=True, help="GCC 14 source tree")
    parser.add_argument("--binutils-src", type=Path, required=True, help="binutils source tree")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.gcc_src.is_dir():
        print(f"missing GCC source tree: {args.gcc_src}", file=sys.stderr)
        return 1
    if not args.binutils_src.is_dir():
        print(f"missing binutils source tree: {args.binutils_src}", file=sys.stderr)
        return 1

    try:
        gcc_files = copy_tree(GCC_BACKEND, args.gcc_src / "gcc", args.force)
        libgcc_files = copy_tree(LIBGCC_BACKEND, args.gcc_src / "libgcc", args.force)
        binutils_files = copy_tree(BINUTILS_BACKEND, args.binutils_src, args.force)
    except FileExistsError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"copied {len(gcc_files)} GCC backend files")
    print(f"copied {len(libgcc_files)} libgcc backend files")
    print(f"copied {len(binutils_files)} binutils backend files")
    print("Manual configure integration is still required; see backend README files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
