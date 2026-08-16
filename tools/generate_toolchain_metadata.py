#!/usr/bin/env python3
"""Generate machine-readable OASIS Base-16 metadata for toolchains."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "toolchain" / "generated" / "oasis-base16t-v1.0.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as file:
        return list(csv.DictReader(file))


def main() -> int:
    opcodes = read_csv(ROOT / "tables" / "opcode-map.csv")
    registers = read_csv(ROOT / "tables" / "registers.csv")
    encoding_fields = read_csv(ROOT / "tables" / "encoding-fields.csv")
    programming_registers = read_csv(ROOT / "tables" / "programming-registers.csv")
    toolchain_targets = read_csv(ROOT / "tables" / "toolchain-targets.csv")

    metadata = {
        "profile": "oasis-base16t-v1.0",
        "base_profile": "oasis-base16-v1.0",
        "target_triple": "oasis16-unknown-none",
        "gcc_target_triple": "oasis16-unknown-elf",
        "tool_alias": "oasis16-elf",
        "data_width": 16,
        "instruction_width": 32,
        "program_counter_width": 8,
        "register_count": 64,
        "direct_address_width": 11,
        "pointer_address_width": 15,
        "address_space_bit": 1,
        "status": "baseline",
        "opcodes": opcodes,
        "registers": registers,
        "encoding_fields": encoding_fields,
        "programming": {
            "access_port_width": 16,
            "recommended_transports": ["jtag", "spi"],
            "registers": programming_registers,
        },
        "toolchain_targets": toolchain_targets,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"generated {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
