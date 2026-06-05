#!/usr/bin/env python3
"""Regression tests for OASIS ELF-to-image conversion."""

from __future__ import annotations

from pathlib import Path
import struct
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ELF2IMG = ROOT / "tools" / "oasis_elf2img.py"
EM_OASIS16 = 0x4F16


def make_exec_elf(words: list[int], start: int) -> bytes:
    text = b"".join(struct.pack("<I", word) for word in words)
    ehsize = 52
    phoff = ehsize
    phentsize = 32
    text_offset = 0x100

    ident = b"\x7fELF" + bytes([1, 1, 1]) + bytes(9)
    header = ident + struct.pack(
        "<HHIIIIIHHHHHH",
        2,
        EM_OASIS16,
        1,
        start,
        phoff,
        0,
        0,
        ehsize,
        phentsize,
        1,
        0,
        0,
        0,
    )
    program_header = struct.pack(
        "<IIIIIIII",
        1,
        text_offset,
        start,
        start,
        len(text),
        len(text),
        1,
        4,
    )
    padding = bytes(text_offset - len(header) - len(program_header))
    return header + program_header + padding + text


def run_elf2img(elf_path: Path, output_format: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ELF2IMG), str(elf_path), "--format", output_format],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> int:
    words = [0x8C400123, 0xFC200000, 0x78000040]

    with tempfile.TemporaryDirectory() as temp_dir:
        elf_path = Path(temp_dir) / "program.elf"
        elf_path.write_bytes(make_exec_elf(words, start=2))

        hex_output = run_elf2img(elf_path, "hex")
        if hex_output != "8c400123\nfc200000\n78000040\n":
            raise AssertionError(hex_output)

        dap_output = run_elf2img(elf_path, "dap16")
        if "W 0004 0002" not in dap_output:
            raise AssertionError("ELF start address was not used for DAP16 image")
        if "W 0005 0123" not in dap_output or "W 0006 8c40" not in dap_output:
            raise AssertionError("first instruction was not emitted little-word first")

    print("ELF-to-image tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
