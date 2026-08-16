#!/usr/bin/env python3
"""Lightweight validation for OASIS compliance YAML files.

This intentionally avoids third-party YAML dependencies. It checks the required
top-level keys and duplicate test names; full semantic execution belongs to an
assembler/emulator harness.
"""

from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests" / "compliance"
OPCODE_TABLE = ROOT / "tables" / "opcode-map.csv"
REQUIRED_KEYS = {"name", "profile", "program", "expect"}
VALID_PROFILES = {
    "oasis-base16-v0.1-draft",
    "oasis-base16t-v0.1-draft",
    "oasis-base16-v0.2-draft",
    "oasis-base16t-v0.2-draft",
    "oasis-base16-v1.0",
    "oasis-base16t-v1.0",
}


def top_level_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        if line.startswith(" ") or not line.strip() or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.add(match.group(1))
    return keys


def scalar_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def indented_block(text: str, header: str, indent: int) -> list[str]:
    lines = text.splitlines()
    start = None
    prefix = " " * indent
    header_line = f"{prefix}{header}:"

    for index, line in enumerate(lines):
        if line == header_line:
            start = index + 1
            break

    if start is None:
        return []

    block: list[str] = []
    for line in lines[start:]:
        if not line.strip():
            block.append(line)
            continue
        current_indent = len(line) - len(line.lstrip(" "))
        if current_indent <= indent:
            break
        block.append(line)

    return block


def mapping_keys(block: list[str], indent: int) -> set[str]:
    keys: set[str] = set()
    prefix = " " * indent
    for line in block:
        if not line.startswith(prefix) or line.startswith(prefix + " "):
            continue
        match = re.match(rf"^ {{{indent}}}([A-Za-z0-9_-]+):", line)
        if match:
            keys.add(match.group(1))
    return keys


def mapping_value(block: list[str], key: str, indent: int) -> str | None:
    prefix = " " * indent
    for line in block:
        if not line.startswith(prefix) or line.startswith(prefix + " "):
            continue
        match = re.match(rf"^ {{{indent}}}{key}:\s*(.+)$", line)
        if match:
            return match.group(1).strip()
    return None


def opcode_mnemonics() -> set[str]:
    with OPCODE_TABLE.open(newline="") as table:
        return {row["mnemonic"].upper() for row in csv.DictReader(table)}


def covered_mnemonics(text: str) -> set[str]:
    covered: set[str] = set()
    in_program = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "program:":
            in_program = True
            continue
        if in_program and re.match(r"^[A-Za-z0-9_-]+:", line):
            in_program = False
        if not in_program or not stripped.startswith("- "):
            continue

        item = stripped[2:].strip().strip('"')
        if item.endswith(":"):
            continue
        parts = item.split(None, 1)
        if parts:
            covered.add(parts[0].upper())

    return covered


def validate_exit_expectation(path: Path, text: str, errors: list[str]) -> None:
    exit_block = indented_block(text, "exit", 2)
    if not exit_block:
        return

    required = {"kind", "symbol", "code_register", "code", "observe"}
    keys = mapping_keys(exit_block, 4)
    missing = required - keys
    if missing:
        errors.append(
            f"{path}: expect.exit missing keys: {', '.join(sorted(missing))}"
        )

    kind = mapping_value(exit_block, "kind", 4)
    if kind not in {"normal", "abort"}:
        errors.append(f"{path}: expect.exit.kind must be normal or abort")

    symbol = mapping_value(exit_block, "symbol", 4)
    if symbol not in {"__oasis_exit", "__oasis_abort"}:
        errors.append(f"{path}: expect.exit.symbol must be __oasis_exit or __oasis_abort")
    elif kind == "normal" and symbol != "__oasis_exit":
        errors.append(f"{path}: expect.exit.kind normal must use __oasis_exit")
    elif kind == "abort" and symbol != "__oasis_abort":
        errors.append(f"{path}: expect.exit.kind abort must use __oasis_abort")

    code_register = mapping_value(exit_block, "code_register", 4)
    if not code_register or not re.match(r"^r([0-9]|[1-5][0-9]|6[0-3])$", code_register):
        errors.append(f"{path}: expect.exit.code_register must be r0 through r63")

    code = mapping_value(exit_block, "code", 4)
    if code and not re.match(r"^(0x[0-9a-fA-F]+|[0-9]+)$", code):
        errors.append(f"{path}: expect.exit.code must be an integer literal")
    elif code and int(code, 0) > 0xffff:
        errors.append(f"{path}: expect.exit.code must fit in 16 bits")

    observe_block = indented_block("\n".join(exit_block), "observe", 4)
    observe_required = {"pc", "register_selector", "register_data"}
    observe_keys = mapping_keys(observe_block, 6)
    observe_missing = observe_required - observe_keys
    if observe_missing:
        errors.append(
            f"{path}: expect.exit.observe missing keys: "
            + ", ".join(sorted(observe_missing))
        )

    expected_observe = {
        "pc": "CORE_PC",
        "register_selector": "GPR_ADDR",
        "register_data": "GPR_RDATA",
    }
    for key, expected in expected_observe.items():
        value = mapping_value(observe_block, key, 6)
        if value and value != expected:
            errors.append(f"{path}: expect.exit.observe.{key} must be {expected}")


def validate_symbol_expectation(path: Path, text: str, errors: list[str]) -> None:
    symbol_block = indented_block(text, "symbols", 2)
    if not symbol_block:
        return

    allowed_symbols = {
        "_start": "runtime",
        "__oasis_exit": "runtime",
        "__oasis_abort": "runtime",
        "__oasis_init_array_start": "linker",
        "__oasis_init_array_end": "linker",
        "__oasis_fini_array_start": "linker",
        "__oasis_fini_array_end": "linker",
        "__oasis_heap_start": "linker",
        "__oasis_heap_end": "linker",
        "__oasis_extmem_start": "linker",
        "__oasis_extmem_end": "linker",
        "__oasis_stack_top": "linker",
        "__oasis_scratch_start": "linker",
        "__oasis_scratch_end": "linker",
        "__oasis_scratch_words": "linker",
    }

    keys = mapping_keys(symbol_block, 4)
    unknown = keys - set(allowed_symbols)
    if unknown:
        errors.append(
            f"{path}: expect.symbols has unknown symbols: "
            + ", ".join(sorted(unknown))
        )

    for symbol, expected_kind in allowed_symbols.items():
        value = mapping_value(symbol_block, symbol, 4)
        if value is None:
            continue
        if value != expected_kind:
            errors.append(
                f"{path}: expect.symbols.{symbol} must be {expected_kind}"
            )


def main() -> int:
    errors: list[str] = []
    names: dict[str, Path] = {}
    files = sorted(TEST_DIR.glob("*.yaml"))
    all_covered: set[str] = set()

    if not files:
        errors.append("no compliance YAML files found")

    for path in files:
        text = path.read_text()
        keys = top_level_keys(text)
        missing = REQUIRED_KEYS - keys
        if missing:
            errors.append(f"{path}: missing top-level keys: {', '.join(sorted(missing))}")

        name = scalar_value(text, "name")
        if not name:
            errors.append(f"{path}: missing scalar test name")
        elif name in names:
            errors.append(f"{path}: duplicate test name {name} also in {names[name]}")
        else:
            names[name] = path

        profile = scalar_value(text, "profile")
        if profile not in VALID_PROFILES:
            errors.append(f"{path}: unexpected profile {profile}")

        validate_exit_expectation(path, text, errors)
        validate_symbol_expectation(path, text, errors)
        all_covered.update(covered_mnemonics(text))

    missing_mnemonics = opcode_mnemonics() - all_covered
    if missing_mnemonics:
        errors.append(
            "missing compliance coverage for: "
            + ", ".join(sorted(missing_mnemonics))
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(files)} compliance tests covering {len(all_covered)} mnemonics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
