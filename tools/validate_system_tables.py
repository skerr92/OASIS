#!/usr/bin/env python3
"""Validate OASIS interrupt, trap, privilege, and system-register tables."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_REGISTERS = ROOT / "tables" / "system-registers.csv"
TRAP_CAUSES = ROOT / "tables" / "trap-causes.csv"
OASIS16P_OPCODES = ROOT / "tables" / "oasis16p-opcode-map.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as source:
        return list(csv.DictReader(source))


def main() -> int:
    errors: list[str] = []
    registers = read_rows(SYSTEM_REGISTERS)
    causes = read_rows(TRAP_CAUSES)
    opcodes = read_rows(OASIS16P_OPCODES)

    register_ids: set[int] = set()
    register_names: set[str] = set()
    for row in registers:
        register_id = int(row["id"], 0)
        if register_id in register_ids:
            errors.append(f"duplicate system-register ID {row['id']}")
        register_ids.add(register_id)
        if register_id > 0xFF:
            errors.append(f"system-register ID exceeds csr8: {row['id']}")
        if row["name"] in register_names:
            errors.append(f"duplicate system-register name {row['name']}")
        register_names.add(row["name"])
        if row["access"] not in {"RO", "RW"}:
            errors.append(f"{row['name']}: invalid access {row['access']}")
        if row["min_privilege"] not in {"U", "M"}:
            errors.append(
                f"{row['name']}: invalid privilege {row['min_privilege']}"
            )

    cause_keys: set[tuple[str, int]] = set()
    cause_names: set[str] = set()
    interrupt_ids: set[int] = set()
    for row in causes:
        cause_id = int(row["id"], 0)
        key = (row["kind"], cause_id)
        if row["kind"] not in {"exception", "interrupt"}:
            errors.append(f"{row['name']}: invalid cause kind {row['kind']}")
        if key in cause_keys:
            errors.append(f"duplicate {row['kind']} cause ID {row['id']}")
        cause_keys.add(key)
        if row["name"] in cause_names:
            errors.append(f"duplicate cause name {row['name']}")
        cause_names.add(row["name"])
        if row["kind"] == "interrupt":
            interrupt_ids.add(cause_id)

    if interrupt_ids != set(range(16)):
        errors.append("interrupt IDs must cover exactly 0x00 through 0x0f")

    required_registers = {
        "STATUS",
        "TVEC",
        "EPC",
        "CAUSE",
        "TVAL",
        "IENABLE",
        "IPENDING",
    }
    missing_registers = required_registers - register_names
    if missing_registers:
        errors.append(
            "missing required system registers: " + ", ".join(sorted(missing_registers))
        )

    subops: set[int] = set()
    for row in opcodes:
        if row["class"] != "00" or row["opcode"] != "1110":
            errors.append(f"{row['mnemonic']}: must use OASIS-16P system group 00:1110")
        subop = int(row["subop"], 2)
        if subop in subops:
            errors.append(f"duplicate OASIS-16P system subop {row['subop']}")
        subops.add(subop)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(
        f"validated {len(registers)} system registers, {len(causes)} trap causes, "
        f"and {len(opcodes)} OASIS-16P instructions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
