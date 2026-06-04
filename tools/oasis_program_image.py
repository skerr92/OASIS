#!/usr/bin/env python3
"""Generate OASIS programming artifacts from assembly source."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import oasis_asm


REG_CONTROL = 0x0000
REG_IMEM_ADDR = 0x0004
REG_IMEM_WDATA_LO = 0x0005
REG_IMEM_WDATA_HI = 0x0006

CTRL_HALT = 1 << 0
CTRL_RESET = 1 << 1
CTRL_IMEM_WRITE = 1 << 2
CTRL_AUTO_INC = 1 << 4


def dap16_script(words: list[int], start_addr: int) -> str:
    lines = [
        "# OASIS DAP16 programming script",
        "# Format: W <register-addr-hex> <data-hex>",
        f"W {REG_CONTROL:04x} {CTRL_HALT | CTRL_RESET:04x}",
        f"W {REG_IMEM_ADDR:04x} {start_addr:04x}",
    ]

    for word in words:
        low = word & 0xFFFF
        high = (word >> 16) & 0xFFFF
        lines.extend(
            [
                f"W {REG_IMEM_WDATA_LO:04x} {low:04x}",
                f"W {REG_IMEM_WDATA_HI:04x} {high:04x}",
                f"W {REG_CONTROL:04x} {CTRL_HALT | CTRL_RESET | CTRL_IMEM_WRITE | CTRL_AUTO_INC:04x}",
            ]
        )

    lines.extend(
        [
            f"W {REG_CONTROL:04x} {CTRL_HALT:04x}",
            f"W {REG_CONTROL:04x} 0000",
        ]
    )
    return "\n".join(lines) + "\n"


def spi16_hex(words: list[int], start_addr: int) -> str:
    script = dap16_script(words, start_addr)
    frames: list[str] = []
    for line in script.splitlines():
        if not line.startswith("W "):
            continue
        _, addr_text, data_text = line.split()
        addr = int(addr_text, 16)
        data = int(data_text, 16)
        frames.append(f"01{addr:04x}{data:04x}")
    return "\n".join(frames) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate OASIS programming images")
    parser.add_argument("input", type=Path, help="input .oas assembly file")
    parser.add_argument("-o", "--output", type=Path, help="output file")
    parser.add_argument(
        "-f",
        "--format",
        choices=["dap16", "spi16-hex"],
        default="dap16",
        help="programming image format",
    )
    parser.add_argument(
        "--start",
        type=lambda value: int(value, 0),
        default=0,
        help="instruction memory start address",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.start < 0 or args.start > oasis_asm.PC_MAX:
        print(f"start address {args.start} out of range 0..{oasis_asm.PC_MAX}", file=sys.stderr)
        return 1

    try:
        words = oasis_asm.assemble(args.input)
    except oasis_asm.AssemblerError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.start + len(words) > oasis_asm.PC_MAX + 1:
        print("program image exceeds instruction memory", file=sys.stderr)
        return 1

    if args.format == "dap16":
        output = dap16_script(words, args.start)
    else:
        output = spi16_hex(words, args.start)

    if args.output:
        args.output.write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
