#!/usr/bin/env python3
"""Tests for toolchain integration scripts and wrappers."""

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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> int:
    cc = run(["bin/oasis-cc"])
    if cc.returncode == 0:
        raise AssertionError("oasis-cc should fail until an installed compiler exists")
    require_contains(cc.stderr, "OASIS_TOOLCHAIN_PREFIX")
    require_contains(cc.stderr, "oasis16-elf-gcc")

    cxx = run(["bin/oasis-c++"])
    if cxx.returncode == 0:
        raise AssertionError("oasis-c++ should fail until an installed compiler exists")
    require_contains(cxx.stderr, "OASIS_TOOLCHAIN_PREFIX")
    require_contains(cxx.stderr, "oasis16-elf-g++")

    generic = run(["toolchain/scripts/build-gcc14.sh", "--help"])
    if generic.returncode != 0:
        raise AssertionError("generic GCC build help should succeed")
    require_contains(generic.stdout, "build-gcc14.sh")

    darwin = run(["toolchain/scripts/build-darwin-gcc14.sh", "--help"])
    if darwin.returncode != 0:
        raise AssertionError("Darwin GCC build help should succeed")
    require_contains(darwin.stdout, "build-darwin-gcc14.sh")

    linux = run(["toolchain/scripts/build-linux-gcc14.sh", "--help"])
    if linux.returncode != 0:
        raise AssertionError("Linux GCC build help should succeed")
    require_contains(linux.stdout, "build-linux-gcc14.sh")

    validate = run(["toolchain/scripts/validate-installed-toolchain.sh", "--help"])
    if validate.returncode != 0:
        raise AssertionError("installed toolchain validation help should succeed")
    require_contains(validate.stdout, "validate-installed-toolchain.sh")

    package_toolchain = run(["toolchain/scripts/package-toolchain-installer.sh", "--help"])
    if package_toolchain.returncode != 0:
        raise AssertionError("toolchain packaging help should succeed")
    require_contains(package_toolchain.stdout, "package-toolchain-installer.sh")

    package_source = run(["toolchain/scripts/package-source-release.sh", "--help"])
    if package_source.returncode != 0:
        raise AssertionError("source packaging help should succeed")
    require_contains(package_source.stdout, "package-source-release.sh")

    dry_validate = run(
        [
            "toolchain/scripts/validate-installed-toolchain.sh",
            "--prefix",
            "/tmp/oasis-missing-prefix",
            "--dry-run",
        ]
    )
    if dry_validate.returncode != 0:
        raise AssertionError(dry_validate.stderr)
    require_contains(dry_validate.stdout, "oasis16-elf-gcc")
    require_contains(dry_validate.stdout, "oasis-elf2img")

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

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        gcc_src = temp / "gcc-14"
        binutils_src = temp / "binutils"

        write(gcc_src / "gcc" / "config.gcc", "case ${target} in\nesac\n")
        write(gcc_src / "libgcc" / "config.host", "case ${host} in\nesac\n")
        write(binutils_src / "bfd" / "config.bfd", "case ${targ} in\n  *)\n    ;;\nesac\n")
        write(binutils_src / "include" / "elf" / "common.h", "#define EM_NONE 0\n")
        write(binutils_src / "bfd" / "archures.c", "const void *bfd_archures_list[] = { 0 };\n")
        write(binutils_src / "bfd" / "reloc.c", "enum bfd_reloc_code_real { BFD_RELOC_NONE };\n")
        write(
            binutils_src / "bfd" / "bfd-in2.h",
            "enum bfd_architecture {\n"
            "  bfd_arch_unknown,\n"
            "  bfd_arch_last\n"
            "};\n"
            "enum bfd_reloc_code_real {\n"
            "  BFD_RELOC_NONE,\n"
            "  BFD_RELOC_UNUSED\n"
            "};\n",
        )
        write(
            binutils_src / "bfd" / "targets.c",
            "static const bfd_target * const _bfd_target_vector[] = {\n"
            "  NULL\n"
            "};\n",
        )
        write(binutils_src / "bfd" / "Makefile.am", "ALL_MACHINES =\nBFD32_BACKENDS =\n")
        write(binutils_src / "bfd" / "Makefile.in", "ALL_MACHINES =\nBFD32_BACKENDS =\n")
        write(binutils_src / "opcodes" / "configure", "case ${target} in\n  *)\n    ;;\nesac\n")
        write(
            binutils_src / "opcodes" / "disassemble.c",
            "extern int print_insn_big_mips (bfd_vma, disassemble_info *);\n"
            "switch (a) {\n"
            "    default:\n"
            "      break;\n"
            "}\n",
        )
        write(binutils_src / "opcodes" / "Makefile.am", "TARGET32_LIBOPCODES_CFILES =\n")
        write(binutils_src / "opcodes" / "Makefile.in", "TARGET32_LIBOPCODES_CFILES =\n")
        write(binutils_src / "gas" / "configure.tgt", "case ${cpu} in\n  *)\n    ;;\nesac\n")
        write(binutils_src / "ld" / "configure.tgt", "case ${targ} in\n  *)\n    ;;\nesac\n")

        apply = run(
            [
                "toolchain/scripts/apply-gcc14-backend.py",
                "--gcc-src",
                str(gcc_src),
                "--binutils-src",
                str(binutils_src),
                "--integrate-config",
            ]
        )
        if apply.returncode != 0:
            raise AssertionError(apply.stderr)

        config_gcc = (gcc_src / "gcc" / "config.gcc").read_text()
        require_contains(config_gcc, "oasis16-*-elf*")
        require_contains((gcc_src / "libgcc" / "config.host").read_text(), "oasis16/t-oasis16")
        require_contains((binutils_src / "bfd" / "config.bfd").read_text(), "oasis16_elf32_vec")
        require_contains((binutils_src / "bfd" / "bfd-in2.h").read_text(), "bfd_arch_oasis16")
        require_contains((binutils_src / "bfd" / "bfd-in2.h").read_text(), "BFD_RELOC_OASIS16_CALL8")
        require_contains((binutils_src / "bfd" / "targets.c").read_text(), "&oasis16_elf32_vec")
        require_contains((binutils_src / "include" / "elf" / "common.h").read_text(), "EM_OASIS16")
        require_contains((binutils_src / "opcodes" / "disassemble.c").read_text(), "print_insn_oasis16")
        require_contains((binutils_src / "opcodes" / "Makefile.in").read_text(), "oasis16-opc.c")
        require_contains((binutils_src / "gas" / "configure.tgt").read_text(), "oasis16-*-elf*")
        require_contains((binutils_src / "ld" / "configure.tgt").read_text(), "targ_emul=oasis16elf")

        reapply = run(
            [
                "toolchain/scripts/apply-gcc14-backend.py",
                "--gcc-src",
                str(gcc_src),
                "--binutils-src",
                str(binutils_src),
                "--integrate-config",
                "--force",
            ]
        )
        if reapply.returncode != 0:
            raise AssertionError(reapply.stderr)
        if (gcc_src / "gcc" / "config.gcc").read_text().count("oasis16-*-elf*") != 1:
            raise AssertionError("config integration should be idempotent")

    print("toolchain integration tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
