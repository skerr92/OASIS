#!/usr/bin/env python3
"""Validate generated instruction documentation coverage."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OPCODE_TABLE = ROOT / "tables" / "opcode-map.csv"
INSTRUCTION_DIR = ROOT / "instructions"
INDEX = INSTRUCTION_DIR / "README.md"


def main() -> int:
    errors: list[str] = []
    with OPCODE_TABLE.open(newline="") as table:
        mnemonics = [row["mnemonic"].upper() for row in csv.DictReader(table)]

    index_text = INDEX.read_text() if INDEX.exists() else ""
    if not index_text:
        errors.append("instructions/README.md is missing or empty")

    for mnemonic in mnemonics:
        path = INSTRUCTION_DIR / f"{mnemonic}.md"
        if not path.exists():
            errors.append(f"missing instruction page: {path}")
            continue

        text = path.read_text()
        required = [f"# {mnemonic}", "## Summary", "## Syntax", "## Encoding", "## Operation"]
        for marker in required:
            if marker not in text:
                errors.append(f"{path}: missing {marker}")

        if f"`{mnemonic}`" not in index_text:
            errors.append(f"instructions/README.md does not list {mnemonic}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(mnemonics)} instruction docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
