#!/usr/bin/env python3
"""Generate OASIS instruction reference pages from tables/opcode-map.csv."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPCODE_TABLE = ROOT / "tables" / "opcode-map.csv"
INSTRUCTION_DIR = ROOT / "instructions"


ENCODING_BY_GROUP = {
    "alu": [
        ("31:30", "class", "`01` ALU/jump class"),
        ("29:26", "opcode", "instruction opcode"),
        ("25:20", "ra", "destination/source register"),
        ("19:14", "rb/imm6", "source register or shift/rotate amount"),
        ("13:6", "target8", "jump target for branch instructions"),
        ("5:0", "reserved", "must be zero"),
    ],
    "branch": [
        ("31:30", "class", "`01` ALU/jump class"),
        ("29:26", "opcode", "instruction opcode"),
        ("25:20", "ra", "source register for conditional branches"),
        ("19:14", "rb", "source register for conditional branches"),
        ("13:6", "target8", "absolute 8-bit instruction target"),
        ("5:0", "reserved", "must be zero"),
    ],
    "register": [
        ("31:30", "class", "`10` register class"),
        ("29:28", "opcode", "instruction opcode"),
        ("27:22", "ra", "destination register"),
        ("21:16", "rb", "source register for MVV"),
        ("15:0", "imm16", "immediate value for MVI"),
    ],
    "memory": [
        ("31:30", "class", "`11` memory class"),
        ("29:28", "opcode", "instruction opcode"),
        ("27:22", "ra/addr9", "register for MVF/MVT or address high field for MSI"),
        ("21:13", "addr9", "data-memory word address for MVF/MVT"),
        ("15:0", "imm16", "immediate value for MSI"),
    ],
}


def table(rows: list[tuple[str, str, str]]) -> str:
    output = ["| Bits | Field | Meaning |", "| ---- | ----- | ------- |"]
    output.extend(f"| `{bits}` | `{field}` | {meaning} |" for bits, field, meaning in rows)
    return "\n".join(output)


def main() -> int:
    INSTRUCTION_DIR.mkdir(exist_ok=True)

    rows = list(csv.DictReader(OPCODE_TABLE.open(newline="")))
    for row in rows:
        example = "\n".join(row["example"].split("|"))
        effects = "\n".join(f"- {item.strip()}" for item in row["effects"].split(";"))
        edge_cases = "\n".join(f"- {item.strip()}" for item in row["edge_cases"].split(";"))
        encoding = table(ENCODING_BY_GROUP[row["group"]])

        page = f"""# {row['mnemonic']}

## Summary

{row['summary']}

## Syntax

```asm
{row['syntax']}
```

## Encoding

Class: `{row['class']}`

Opcode: `{row['opcode']}`

{encoding}

## Operation

```text
{row['operation']}
```

## Effects

{effects}

## Edge Cases

{edge_cases}

## Example

```asm
{example}
```
"""
        (INSTRUCTION_DIR / f"{row['mnemonic']}.md").write_text(page)

    index_rows = "\n".join(
        f"| `{row['mnemonic']}` | [{row['mnemonic']}.md]({row['mnemonic']}.md) |"
        for row in rows
    )
    (INSTRUCTION_DIR / "README.md").write_text(
        "# OASIS v0.1 Instruction Reference\n\n"
        "These pages are generated from `tables/opcode-map.csv`.\n\n"
        "| Instruction | Page |\n"
        "| ----------- | ---- |\n"
        f"{index_rows}\n"
    )

    print(f"generated {len(rows)} instruction pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
