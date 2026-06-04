#!/usr/bin/env python3
"""Lightweight validation for OASIS compliance YAML files.

This intentionally avoids third-party YAML dependencies. It checks the required
top-level keys and duplicate test names; full semantic execution belongs to an
assembler/emulator harness.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests" / "compliance"
REQUIRED_KEYS = {"name", "profile", "program", "expect"}
VALID_PROFILES = {"oasis-base16-v0.1-draft", "oasis-base16t-v0.1-draft"}


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


def main() -> int:
    errors: list[str] = []
    names: dict[str, Path] = {}
    files = sorted(TEST_DIR.glob("*.yaml"))

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

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(files)} compliance tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
