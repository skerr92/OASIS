#!/usr/bin/env python3
"""Validate OASIS opcode table consistency."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OPCODE_TABLE = ROOT / "tables" / "opcode-map.csv"


def main() -> int:
    seen: dict[tuple[str, str], str] = {}
    errors: list[str] = []

    with OPCODE_TABLE.open(newline="") as table:
        for row in csv.DictReader(table):
            mnemonic = row["mnemonic"]
            key = (row["class"], row["opcode"])

            if key in seen:
                errors.append(
                    f"duplicate class/opcode {key[0]}/{key[1]}: "
                    f"{seen[key]} and {mnemonic}"
                )
            else:
                seen[key] = mnemonic

            if mnemonic != mnemonic.upper():
                errors.append(f"{mnemonic}: mnemonic must be uppercase")

            if row["class"] not in {"01", "10", "11"}:
                errors.append(f"{mnemonic}: invalid class {row['class']}")

            expected_opcode_width = 4 if row["class"] == "01" else 2
            if len(row["opcode"]) != expected_opcode_width:
                errors.append(
                    f"{mnemonic}: opcode {row['opcode']} must be "
                    f"{expected_opcode_width} bits for class {row['class']}"
                )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(seen)} opcode entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
