#!/usr/bin/env python3
"""Validate draft OASIS-32 machine-readable tables."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables" / "oasis32"


def read_csv(name: str) -> list[dict[str, str]]:
    path = TABLE_DIR / name
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_hex_nibble(value: str, field: str) -> int:
    try:
        parsed = int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be hex, got {value!r}") from exc
    if parsed < 0 or parsed > 0xF:
        raise ValueError(f"{field} must fit in 4 bits, got {value!r}")
    return parsed


def require_columns(rows: list[dict[str, str]], columns: set[str], table: str) -> None:
    if not rows:
        raise ValueError(f"{table} has no rows")
    missing = columns - set(rows[0])
    if missing:
        raise ValueError(f"{table} missing columns: {', '.join(sorted(missing))}")


def validate_formats() -> set[str]:
    rows = read_csv("encoding-formats.csv")
    require_columns(
        rows,
        {
            "format",
            "description",
            "bits_63_60",
            "bits_59_56",
            "bits_55_48",
            "bits_47_40",
            "bits_39_32",
            "bits_31_0",
        },
        "encoding-formats.csv",
    )

    formats: set[str] = set()
    for row in rows:
        fmt = row["format"]
        if not fmt:
            raise ValueError("encoding format with empty name")
        if fmt in formats:
            raise ValueError(f"duplicate encoding format: {fmt}")
        formats.add(fmt)
    return formats


def validate_extensions() -> tuple[set[str], set[int]]:
    rows = read_csv("extensions.csv")
    require_columns(
        rows,
        {"extension", "class", "name", "status", "description"},
        "extensions.csv",
    )

    extensions: set[str] = set()
    classes: set[int] = set()
    for row in rows:
        extension = row["extension"]
        cls = parse_hex_nibble(row["class"], f"{extension}.class")
        extensions.add(extension)
        classes.add(cls)
        if row["status"] not in {"draft", "reserved", "experimental"}:
            raise ValueError(f"{extension} has invalid status {row['status']!r}")
    return extensions, classes


def validate_registers() -> None:
    rows = read_csv("registers.csv")
    require_columns(
        rows,
        {"id", "name", "alias", "role", "volatility", "status"},
        "registers.csv",
    )

    ids: set[int] = set()
    names: set[str] = set()
    aliases: set[str] = set()
    for row in rows:
        reg_id = int(row["id"], 10)
        if reg_id < 0 or reg_id > 63:
            raise ValueError(f"Base-32 register id out of range: {reg_id}")
        if reg_id in ids:
            raise ValueError(f"duplicate register id: {reg_id}")
        ids.add(reg_id)

        name = row["name"]
        alias = row["alias"]
        if name in names:
            raise ValueError(f"duplicate register name: {name}")
        if alias in aliases:
            raise ValueError(f"duplicate register alias: {alias}")
        names.add(name)
        aliases.add(alias)

    expected = set(range(64))
    missing = expected - ids
    if missing:
        raise ValueError(f"missing register ids: {sorted(missing)}")


def validate_opcodes(formats: set[str], extensions: set[str], classes: set[int]) -> None:
    rows = read_csv("opcode-map.csv")
    require_columns(
        rows,
        {"mnemonic", "class", "op", "format", "extension", "status", "description"},
        "opcode-map.csv",
    )

    mnemonics: set[str] = set()
    encodings: set[tuple[int, int]] = set()
    for row in rows:
        mnemonic = row["mnemonic"]
        cls = parse_hex_nibble(row["class"], f"{mnemonic}.class")
        op = parse_hex_nibble(row["op"], f"{mnemonic}.op")

        if mnemonic in mnemonics:
            raise ValueError(f"duplicate mnemonic: {mnemonic}")
        mnemonics.add(mnemonic)

        encoding = (cls, op)
        if encoding in encodings:
            raise ValueError(f"duplicate class/op encoding: {mnemonic} 0x{cls:x}/0x{op:x}")
        encodings.add(encoding)

        if cls not in classes:
            raise ValueError(f"{mnemonic} uses undefined class 0x{cls:x}")
        if row["format"] not in formats:
            raise ValueError(f"{mnemonic} uses undefined format {row['format']!r}")
        if row["extension"] not in extensions:
            raise ValueError(f"{mnemonic} uses undefined extension {row['extension']!r}")
        if row["status"] not in {"draft", "reserved", "experimental"}:
            raise ValueError(f"{mnemonic} has invalid status {row['status']!r}")


def main() -> int:
    formats = validate_formats()
    extensions, classes = validate_extensions()
    validate_registers()
    validate_opcodes(formats, extensions, classes)
    print("validated OASIS-32 draft tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
