#!/usr/bin/env python3
"""Validate OASIS binutils backend skeleton consistency."""

from __future__ import annotations

import csv
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
OPCODE_TABLE = ROOT / "tables" / "opcode-map.csv"
BINUTILS = ROOT / "toolchain" / "binutils" / "backend"


def main() -> int:
    errors: list[str] = []

    with OPCODE_TABLE.open(newline="") as table:
        isa_mnemonics = {row["mnemonic"].upper() for row in csv.DictReader(table)}

    opcode_c = (BINUTILS / "opcodes" / "oasis16-opc.c").read_text()
    backend_mnemonics = {
        match.group(1).upper()
        for match in re.finditer(r'\{\s*"([A-Za-z0-9]+)"\s*,', opcode_c)
    }

    missing = isa_mnemonics - backend_mnemonics
    extra = backend_mnemonics - isa_mnemonics
    if missing:
        errors.append("binutils opcode table missing: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("binutils opcode table has unknown mnemonics: " + ", ".join(sorted(extra)))

    gas = (BINUTILS / "gas" / "config" / "tc-oasis16.c").read_text()
    if "not implemented yet" in gas:
        errors.append("GAS backend still contains placeholder text")
    for token in ["md_assemble", "oasis16_encode_instruction", "tc_gen_reloc"]:
        if token not in gas:
            errors.append(f"GAS backend missing {token}")
    if not (BINUTILS / "gas" / "config" / "tc-oasis16.h").exists():
        errors.append("GAS backend missing tc-oasis16.h")

    opcode_header = (BINUTILS / "include" / "opcode" / "oasis16.h").read_text()
    for token in [
        "OASIS16_INSN_SIZE",
        "oasis16_decode_instruction",
        "oasis16_print_instruction",
        "print_insn_oasis16",
    ]:
        if token not in opcode_header:
            errors.append(f"opcode header missing {token}")

    for token in [
        "oasis16_decode_instruction",
        "oasis16_print_instruction",
        "print_insn_oasis16",
    ]:
        if token not in opcode_c:
            errors.append(f"opcodes backend missing {token}")

    elf_header = (BINUTILS / "include" / "elf" / "oasis16.h").read_text()
    for reloc in [
        "R_OASIS16_16",
        "R_OASIS16_ABS16",
        "R_OASIS16_ADDR11",
        "R_OASIS16_MSI_ADDR11",
        "R_OASIS16_TARGET8",
        "R_OASIS16_PCREL8",
        "R_OASIS16_CALL8",
        "R_OASIS16_CALL",
    ]:
        if reloc not in elf_header:
            errors.append(f"ELF header missing {reloc}")

    elf_bfd = (BINUTILS / "bfd" / "elf32-oasis16.c").read_text()
    for reloc in [
        "R_OASIS16_16",
        "R_OASIS16_ADDR11",
        "R_OASIS16_MSI_ADDR11",
        "R_OASIS16_TARGET8",
        "R_OASIS16_CALL8",
    ]:
        if reloc not in elf_bfd:
            errors.append(f"BFD backend missing howto for {reloc}")

    required_files = [
        BINUTILS / "ld" / "emulparams" / "oasis16elf.sh",
        BINUTILS / "ld" / "scripttempl" / "oasis16.sc",
        BINUTILS / "bfd" / "cpu-oasis16.c",
        BINUTILS / "bfd" / "elf32-oasis16.c",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"missing binutils backend file: {path}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated binutils backend for {len(isa_mnemonics)} mnemonics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
