#!/usr/bin/env python3
"""Copy and optionally wire OASIS GCC/binutils backend files into source trees."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]
GCC_BACKEND = ROOT / "toolchain" / "gcc14" / "backend" / "gcc"
LIBGCC_BACKEND = ROOT / "toolchain" / "gcc14" / "backend" / "libgcc"
BINUTILS_BACKEND = ROOT / "toolchain" / "binutils" / "backend"


class IntegrationError(RuntimeError):
    pass


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


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.write_text(text)


def append_if_missing(path: Path, token: str, addition: str) -> bool:
    text = read_text(path)
    if token in text:
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + addition)
    return True


def insert_before_marker(path: Path, token: str, marker: str, addition: str) -> bool:
    text = read_text(path)
    if token in text:
        return False
    if marker not in text:
        raise IntegrationError(f"{path} missing marker {marker!r}")
    write_text(path, text.replace(marker, addition + marker, 1))
    return True


def insert_before_first_marker(
    path: Path, token: str, markers: tuple[str, ...], addition: str
) -> bool:
    text = read_text(path)
    if token in text:
        return False
    for marker in markers:
        if marker in text:
            write_text(path, text.replace(marker, addition + marker, 1))
            return True
    raise IntegrationError(f"{path} missing markers {markers!r}")


def replace_once(path: Path, token: str, old: str, new: str) -> bool:
    text = read_text(path)
    if token in text:
        return False
    if old not in text:
        raise IntegrationError(f"{path} missing marker {old!r}")
    write_text(path, text.replace(old, new, 1))
    return True


def insert_configure_vector(path: Path) -> bool:
    return insert_before_marker(
        path,
        "oasis16_elf32_vec)",
        "    xstormy16_elf32_vec)",
        "    oasis16_elf32_vec)          tb=\"$tb elf32-oasis16.lo elf32.lo $elf\" ;;\n",
    )


def insert_archures_extern(path: Path) -> bool:
    token = "extern const bfd_arch_info_type bfd_oasis16_arch;\n"
    text = read_text(path)
    if token in text:
        text = text.replace(token, "")
    marker = "static const bfd_arch_info_type * const bfd_archures_list[]"
    if marker in text:
        write_text(path, text.replace(marker, token + "\n" + marker, 1))
    else:
        write_text(path, token + "\n" + text)
    return True


def insert_reloc_docs(path: Path) -> bool:
    bad_addition = (
        "\n/* OASIS Base-16T relocations. */\n"
        "  BFD_RELOC_OASIS16_16,\n"
        "  BFD_RELOC_OASIS16_ADDR9,\n"
        "  BFD_RELOC_OASIS16_TARGET8,\n"
        "  BFD_RELOC_OASIS16_CALL8,\n"
    )
    addition = (
        "ENUMX\n"
        "  BFD_RELOC_OASIS16_16\n"
        "ENUMX\n"
        "  BFD_RELOC_OASIS16_ADDR9\n"
        "ENUMX\n"
        "  BFD_RELOC_OASIS16_TARGET8\n"
        "ENUMX\n"
        "  BFD_RELOC_OASIS16_CALL8\n"
        "ENUMDOC\n"
        "  OASIS Base-16T relocations.\n"
        "\n"
    )
    text = read_text(path).replace(bad_addition, "")
    if "BFD_RELOC_OASIS16_CALL8\nENUMDOC" in text:
        return False
    marker = "ENDSENUM\n  BFD_RELOC_UNUSED"
    if marker not in text:
        return False
    write_text(path, text.replace(marker, addition + marker, 1))
    return True


def insert_opcodes_arch(path: Path) -> bool:
    if "bfd_or1k_arch)" not in read_text(path):
        return False
    return insert_before_marker(
        path,
        "bfd_oasis16_arch)",
        "\tbfd_or1k_arch)",
        "\tbfd_oasis16_arch)\tta=\"$ta oasis16-opc.lo\" ;;\n",
    )


def insert_ld_emulation_source(path: Path) -> bool:
    return insert_before_marker(
        path,
        "eoasis16elf.c",
        "\tepjelf.c",
        "\teoasis16elf.c \\\n",
    )


def insert_bfd_config_target(path: Path) -> bool:
    addition = (
        "  oasis16-*-elf*)\n"
        "    targ_defvec=oasis16_elf32_vec\n"
        "    targ_selvecs=\n"
        "    ;;\n"
    )
    text = read_text(path)
    if addition in text:
        text = text.replace(addition, "")
    marker = "  or1k-*-elf | or1k-*-linux* | or1k-*-rtems*)"
    fallback = "  *)\n"
    if marker in text:
        write_text(path, text.replace(marker, addition + marker, 1))
    elif fallback in text:
        write_text(path, text.replace(fallback, addition + fallback, 1))
    elif "esac\n" in text:
        write_text(path, text.replace("esac\n", addition + "esac\n", 1))
    else:
        raise IntegrationError(f"{path} missing marker {marker!r}")
    return True


def patch_if_exists(path: Path, patcher) -> bool:
    if not path.exists():
        return False
    return patcher(path)


def integrate_config_sub(source_root: Path) -> bool:
    config_sub = source_root / "config.sub"
    return patch_if_exists(
        config_sub,
        lambda path: insert_before_marker(
            path,
            "| oasis16 \\",
            "\t\t\t| or1k* \\",
            "\t\t\t| oasis16 \\\n",
        ),
    )


def integrate_gcc(gcc_src: Path) -> list[str]:
    changes: list[str] = []

    if integrate_config_sub(gcc_src):
        changes.append("config.sub")

    config_gcc = gcc_src / "gcc" / "config.gcc"
    if patch_if_exists(
        config_gcc,
        lambda path: integrate_gcc_config_gcc(path),
    ):
        changes.append("gcc/config.gcc")

    config_host = gcc_src / "libgcc" / "config.host"
    if patch_if_exists(
        config_host,
        lambda path: integrate_libgcc_config_host(path),
    ):
        changes.append("libgcc/config.host")

    return changes


def integrate_libgcc_config_host(path: Path) -> bool:
    cpu_block = (
        "oasis16-*-elf*)\n"
        "\ttmake_file=\"${tmake_file} oasis16/t-oasis16\"\n"
        "\t;;\n"
    )
    target_block = (
        "oasis16-*-elf*)\n"
        "\ttmake_file=\"${tmake_file} oasis16/t-oasis16\"\n"
        "\t;;\n"
    )
    target_marker = "m32c-*-elf*)\n"

    text = read_text(path)
    changed = False

    first_esac = text.find("esac\n")
    if first_esac != -1:
        before = text[:first_esac]
        after = text[first_esac:]
        if cpu_block in before:
            before = before.replace(cpu_block, "")
            text = before + after
            changed = True

    if target_block in text[text.find(target_marker) if target_marker in text else 0:]:
        return changed

    if target_marker in text:
        write_text(path, text.replace(target_marker, target_block + target_marker, 1))
    elif "esac\n" in text:
        write_text(path, text.replace("esac\n", target_block + "esac\n", 1))
    else:
        raise IntegrationError(f"{path} missing marker {target_marker!r}")
    return True


def integrate_gcc_config_gcc(path: Path) -> bool:
    text = path.read_text()
    cpu_block = (
        "oasis16-*-elf*)\n"
        "\ttm_file=\"elfos.h newlib-stdint.h oasis16/oasis16.h\"\n"
        "\ttmake_file=\"oasis16/t-oasis16\"\n"
        "\tuse_gcc_stdint=wrap\n"
        "\t;;\n"
    )
    old_cpu_replacement = (
        "oasis16-*-elf*)\n"
        "\ttm_file=\"elfos.h newlib-stdint.h oasis16/oasis16.h\"\n"
        "\ttmake_file=\"oasis16/t-oasis16\"\n"
        "\textra_objs=\"oasis16.o\"\n"
        "\tuse_gcc_stdint=wrap\n"
        "\t;;\n"
    )
    cpu_replacement = (
        "oasis16-*-elf*)\n"
        "\ttm_file=\"elfos.h newlib-stdint.h oasis16/oasis16.h\"\n"
        "\ttmake_file=\"oasis16/t-oasis16\"\n"
        "\textra_objs=\"oasis16.o\"\n"
        "\ttarget_has_targetm_common=no\n"
        "\tuse_gcc_stdint=wrap\n"
        "\t;;\n"
    )
    target_replacement = (
        "oasis16-*-elf*)\n"
        "\ttm_file=\"elfos.h newlib-stdint.h oasis16/oasis16.h\"\n"
        "\ttm_p_file=\"oasis16/oasis16-protos.h\"\n"
        "\tmd_file=\"oasis16/oasis16.md\"\n"
        "\tout_file=\"oasis16/oasis16.cc\"\n"
        "\ttmake_file=\"oasis16/t-oasis16\"\n"
        "\textra_objs=\"oasis16.o\"\n"
        "\ttarget_has_targetm_common=no\n"
        "\tuse_gcc_stdint=wrap\n"
        "\t;;\n"
    )
    old_target_with_extra_options = target_replacement.replace(
        "\tout_file=\"oasis16/oasis16.cc\"\n",
        "\tout_file=\"oasis16/oasis16.cc\"\n"
        "\textra_options=\"${extra_options} oasis16/oasis16.opt\"\n",
    )
    old_target_replacement = target_replacement.replace(
        "\ttarget_has_targetm_common=no\n", ""
    )
    old_target_replacement_with_extra_options = old_target_with_extra_options.replace(
        "\ttarget_has_targetm_common=no\n", ""
    )

    changed = False
    for stale in (
        cpu_block,
        old_cpu_replacement,
        cpu_replacement,
        old_target_replacement,
        old_target_with_extra_options,
        old_target_replacement_with_extra_options,
    ):
        if stale in text:
            text = text.replace(stale, "")
            changed = True

    cpu_marker = "m32c*-*-*)\n"
    if cpu_marker in text and cpu_replacement not in text:
        text = text.replace(cpu_marker, cpu_replacement + cpu_marker, 1)
        changed = True

    target_marker = "xstormy16-*-elf)\n"
    if target_marker in text and target_replacement not in text:
        text = text.replace(target_marker, target_replacement + target_marker, 1)
        changed = True
    elif target_marker not in text:
        fallback = target_replacement if cpu_marker not in text else cpu_replacement
        if fallback not in text and "esac\n" in text:
            text = text.replace("esac\n", fallback + "esac\n", 1)
            changed = True
        elif fallback not in text:
            raise RuntimeError(
                f"{path}: marker not found: {target_marker.strip()} or esac"
            )

    if changed:
        path.write_text(text)
    return changed


def integrate_binutils(binutils_src: Path) -> list[str]:
    changes: list[str] = []

    if integrate_config_sub(binutils_src):
        changes.append("config.sub")

    config_bfd = binutils_src / "bfd" / "config.bfd"
    if patch_if_exists(config_bfd, insert_bfd_config_target):
        changes.append("bfd/config.bfd")

    common_h = binutils_src / "include" / "elf" / "common.h"
    if patch_if_exists(
        common_h,
        lambda path: append_if_missing(
            path,
            "EM_OASIS16",
            "\n/* Experimental OASIS Base-16T machine number. */\n#define EM_OASIS16 0x4f16\n",
        ),
    ):
        changes.append("include/elf/common.h")

    archures_c = binutils_src / "bfd" / "archures.c"
    if patch_if_exists(archures_c, insert_archures_extern):
        changes.append("bfd/archures.c")

    elf_bfd_h = binutils_src / "bfd" / "elf-bfd.h"
    if patch_if_exists(
        elf_bfd_h,
        lambda path: insert_before_marker(
            path,
            "OASIS16_ELF_DATA",
            "  OR1K_ELF_DATA,",
            "  OASIS16_ELF_DATA,\n",
        ),
    ):
        changes.append("bfd/elf-bfd.h")

    reloc_c = binutils_src / "bfd" / "reloc.c"
    if patch_if_exists(reloc_c, insert_reloc_docs):
        changes.append("bfd/reloc.c")

    bfd_in2_h = binutils_src / "bfd" / "bfd-in2.h"
    if patch_if_exists(
        bfd_in2_h,
        lambda path: insert_before_marker(
            path,
            "bfd_arch_oasis16",
            "  bfd_arch_last",
            "  bfd_arch_oasis16,\n",
        ),
    ):
        changes.append("bfd/bfd-in2.h:arch")
    if patch_if_exists(
        bfd_in2_h,
        lambda path: insert_before_marker(
            path,
            "BFD_RELOC_OASIS16_CALL8",
            "  BFD_RELOC_UNUSED",
            (
                "  BFD_RELOC_OASIS16_16,\n"
                "  BFD_RELOC_OASIS16_ADDR9,\n"
                "  BFD_RELOC_OASIS16_TARGET8,\n"
                "  BFD_RELOC_OASIS16_CALL8,\n"
            ),
        ),
    ):
        changes.append("bfd/bfd-in2.h:reloc")

    targets_c = binutils_src / "bfd" / "targets.c"
    if patch_if_exists(
        targets_c,
        lambda path: insert_before_marker(
            path,
            "extern const bfd_target oasis16_elf32_vec",
            "static const bfd_target * const _bfd_target_vector[]",
            "extern const bfd_target oasis16_elf32_vec;\n",
        ),
    ):
        changes.append("bfd/targets.c:extern")
    if patch_if_exists(
        targets_c,
        lambda path: insert_before_first_marker(
            path,
            "&oasis16_elf32_vec",
            ("\tNULL /* end of list marker */", "  NULL\n"),
            "  &oasis16_elf32_vec,\n",
        ),
    ):
        changes.append("bfd/targets.c:vector")

    bfd_makefile = binutils_src / "bfd" / "Makefile.am"
    if patch_if_exists(
        bfd_makefile,
        lambda path: append_if_missing(
            path,
            "cpu-oasis16.lo",
            (
                "\n# OASIS Base-16T backend objects.\n"
                "ALL_MACHINES += cpu-oasis16.lo\n"
                "BFD32_BACKENDS += elf32-oasis16.lo\n"
            ),
        ),
    ):
        changes.append("bfd/Makefile.am")

    bfd_makefile_in = binutils_src / "bfd" / "Makefile.in"
    if patch_if_exists(
        bfd_makefile_in,
        lambda path: append_if_missing(
            path,
            "cpu-oasis16.lo",
            (
                "\n# OASIS Base-16T backend objects.\n"
                "ALL_MACHINES += cpu-oasis16.lo\n"
                "BFD32_BACKENDS += elf32-oasis16.lo\n"
            ),
        ),
    ):
        changes.append("bfd/Makefile.in")

    bfd_configure_ac = binutils_src / "bfd" / "configure.ac"
    if patch_if_exists(bfd_configure_ac, insert_configure_vector):
        changes.append("bfd/configure.ac")

    bfd_configure = binutils_src / "bfd" / "configure"
    if patch_if_exists(bfd_configure, insert_configure_vector):
        changes.append("bfd/configure")

    opcodes_configure = binutils_src / "opcodes" / "configure"
    if patch_if_exists(
        opcodes_configure,
        lambda path: insert_before_marker(
            path,
            "oasis16-*-elf*",
            "  *)\n",
            "  oasis16-*-elf*) ta=oasis16 ;;\n",
        ),
    ):
        changes.append("opcodes/configure")

    opcodes_configure_ac = binutils_src / "opcodes" / "configure.ac"
    if patch_if_exists(opcodes_configure_ac, insert_opcodes_arch):
        changes.append("opcodes/configure.ac")

    if patch_if_exists(opcodes_configure, insert_opcodes_arch):
        changes.append("opcodes/configure:arch")

    disassemble_c = binutils_src / "opcodes" / "disassemble.c"
    if patch_if_exists(
        disassemble_c,
        lambda path: insert_before_first_marker(
            path,
            "print_insn_oasis16",
            ("disassembler_ftype\n", "switch ("),
            (
                "extern int print_insn_oasis16 (bfd_vma, disassemble_info *);\n"
            ),
        ),
    ):
        changes.append("opcodes/disassemble.c:extern")
    if patch_if_exists(
        disassemble_c,
        lambda path: insert_before_marker(
            path,
            "bfd_arch_oasis16",
            "    default:\n",
            "    case bfd_arch_oasis16:\n      disassemble = print_insn_oasis16;\n      break;\n",
        ),
    ):
        changes.append("opcodes/disassemble.c:switch")

    opcodes_makefile = binutils_src / "opcodes" / "Makefile.am"
    if patch_if_exists(
        opcodes_makefile,
        lambda path: append_if_missing(
            path,
            "oasis16-opc.c",
            "\nTARGET32_LIBOPCODES_CFILES += oasis16-opc.c\n",
        ),
    ):
        changes.append("opcodes/Makefile.am")

    opcodes_makefile_in = binutils_src / "opcodes" / "Makefile.in"
    if patch_if_exists(
        opcodes_makefile_in,
        lambda path: append_if_missing(
            path,
            "oasis16-opc.c",
            "\nTARGET32_LIBOPCODES_CFILES += oasis16-opc.c\n",
        ),
    ):
        changes.append("opcodes/Makefile.in")

    gas_configure = binutils_src / "gas" / "configure.tgt"
    if patch_if_exists(
        gas_configure,
        lambda path: insert_before_first_marker(
            path,
            "oasis16-*-elf*",
            ("  *-*-elf | *-*-rtems* | *-*-sysv4*)", "  *)\n", "esac\n"),
            "  oasis16-*-elf*) fmt=elf ;;\n",
        ),
    ):
        changes.append("gas/configure.tgt")

    ld_configure = binutils_src / "ld" / "configure.tgt"
    if patch_if_exists(
        ld_configure,
        lambda path: insert_before_first_marker(
            path,
            "oasis16-*-elf*",
            (
                "or1k-*-elf | or1knd-*-elf | or1k-*-rtems* | or1knd-*-rtems*)",
                "  *)\n",
                "esac\n",
            ),
            "oasis16-*-elf*) targ_emul=oasis16elf ;;\n",
        ),
    ):
        changes.append("ld/configure.tgt")

    ld_makefile_am = binutils_src / "ld" / "Makefile.am"
    if patch_if_exists(ld_makefile_am, insert_ld_emulation_source):
        changes.append("ld/Makefile.am")

    ld_makefile_in = binutils_src / "ld" / "Makefile.in"
    if patch_if_exists(ld_makefile_in, insert_ld_emulation_source):
        changes.append("ld/Makefile.in")

    return changes


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gcc-src", type=Path, required=True, help="GCC 14 source tree")
    parser.add_argument("--binutils-src", type=Path, required=True, help="binutils source tree")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument(
        "--integrate-config",
        action="store_true",
        help="patch standard GCC/binutils configure files when they exist",
    )
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
        gcc_changes = integrate_gcc(args.gcc_src) if args.integrate_config else []
        binutils_changes = integrate_binutils(args.binutils_src) if args.integrate_config else []
    except (FileExistsError, IntegrationError) as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"copied {len(gcc_files)} GCC backend files")
    print(f"copied {len(libgcc_files)} libgcc backend files")
    print(f"copied {len(binutils_files)} binutils backend files")
    if args.integrate_config:
        print(f"patched {len(gcc_changes)} GCC configure files")
        print(f"patched {len(binutils_changes)} binutils configure files")
    else:
        print("Configure integration skipped; pass --integrate-config to patch source trees.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
