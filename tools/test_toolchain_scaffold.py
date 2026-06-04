#!/usr/bin/env python3
"""Tests for toolchain scaffold scripts and wrappers."""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, check=False, capture_output=True, text=True)


def require_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"expected {expected!r} in {text!r}")


def main() -> int:
    cc = run(["bin/oasis-cc"])
    if cc.returncode == 0:
        raise AssertionError("oasis-cc should fail until a backend exists")
    require_contains(cc.stderr, "oasis16-unknown-elf")
    require_contains(cc.stderr, "Darwin/macOS")

    cxx = run(["bin/oasis-c++"])
    if cxx.returncode == 0:
        raise AssertionError("oasis-c++ should fail until a backend exists")
    require_contains(cxx.stderr, "oasis16-unknown-elf")

    generic = run(["toolchain/scripts/build-gcc14.sh", "--help"])
    if generic.returncode != 0:
        raise AssertionError("generic GCC scaffold help should succeed")
    require_contains(generic.stdout, "build-gcc14.sh")

    darwin = run(["toolchain/scripts/build-darwin-gcc14.sh", "--help"])
    if darwin.returncode != 0:
        raise AssertionError("Darwin GCC scaffold help should succeed")
    require_contains(darwin.stdout, "build-darwin-gcc14.sh")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        gcc_src = temp / "gcc-14"
        binutils_src = temp / "binutils"
        (gcc_src / "gcc").mkdir(parents=True)
        (gcc_src / "libgcc").mkdir(parents=True)
        binutils_src.mkdir()

        apply = run(
            [
                "toolchain/scripts/apply-gcc14-backend.py",
                "--gcc-src",
                str(gcc_src),
                "--binutils-src",
                str(binutils_src),
            ]
        )
        if apply.returncode != 0:
            raise AssertionError(apply.stderr)
        if not (gcc_src / "gcc" / "config" / "oasis16" / "oasis16.md").exists():
            raise AssertionError("GCC backend skeleton was not copied")
        if not (gcc_src / "libgcc" / "config" / "oasis16" / "lib1funcs.S").exists():
            raise AssertionError("libgcc backend skeleton was not copied")
        if not (binutils_src / "include" / "opcode" / "oasis16.h").exists():
            raise AssertionError("binutils backend skeleton was not copied")

    print("toolchain scaffold tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
