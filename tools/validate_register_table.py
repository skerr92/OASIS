#!/usr/bin/env python3
"""Validate OASIS register table consistency."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTER_TABLE = ROOT / "tables" / "registers.csv"


def main() -> int:
    errors: list[str] = []
    names: set[str] = set()
    numbers: set[int] = set()

    with REGISTER_TABLE.open(newline="") as table:
        rows = list(csv.DictReader(table))

    if len(rows) != 64:
        errors.append(f"expected 64 registers, found {len(rows)}")

    for row in rows:
        name = row["name"]
        number = int(row["number"])
        width = int(row["width"])

        if name in names:
            errors.append(f"duplicate register name {name}")
        names.add(name)

        if number in numbers:
            errors.append(f"duplicate register number {number}")
        numbers.add(number)

        if name != f"r{number}":
            errors.append(f"{name}: expected name r{number}")

        if number < 0 or number > 63:
            errors.append(f"{name}: register number out of range: {number}")

        if width != 16:
            errors.append(f"{name}: expected width 16, got {width}")

    missing = set(range(64)) - numbers
    if missing:
        errors.append(f"missing register numbers: {sorted(missing)}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("validated 64 registers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
