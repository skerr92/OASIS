#!/usr/bin/env python3
"""Regression tests for the OASIS Base-16 assembler."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ASM = ROOT / "tools" / "oasis_asm.py"
PROGRAM_IMAGE = ROOT / "tools" / "oasis_program_image.py"


def run_asm(source: Path, output_format: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ASM), str(source), "--format", output_format],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def assert_file(source: Path, expected: Path, output_format: str) -> None:
    actual = run_asm(source, output_format)
    want = expected.read_text()
    if actual != want:
        raise AssertionError(
            f"{source} {output_format} mismatch\nexpected:\n{want}\nactual:\n{actual}"
        )


def assert_error(source_text: str, expected_text: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".oas", delete=False) as temp:
        temp.write(source_text)
        temp_path = Path(temp.name)

    try:
        result = subprocess.run(
            [sys.executable, str(ASM), str(temp_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            raise AssertionError("assembler succeeded unexpectedly")
        if expected_text not in result.stderr:
            raise AssertionError(
                f"expected error containing {expected_text!r}, got {result.stderr!r}"
            )
    finally:
        temp_path.unlink()


def run_program_image(source: Path, output_format: str) -> str:
    result = subprocess.run(
        [sys.executable, str(PROGRAM_IMAGE), str(source), "--format", output_format],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def assert_program_image(source: Path, expected: Path, output_format: str) -> None:
    actual = run_program_image(source, output_format)
    want = expected.read_text()
    if actual != want:
        raise AssertionError(
            f"{source} {output_format} mismatch\nexpected:\n{want}\nactual:\n{actual}"
        )


def main() -> int:
    assert_file(
        ROOT / "examples" / "base16" / "add_store.oas",
        ROOT / "tests" / "assembler" / "add_store.expected.binstr",
        "binstr",
    )
    assert_file(
        ROOT / "examples" / "base16" / "add_store.oas",
        ROOT / "tests" / "assembler" / "add_store.expected.hex",
        "hex",
    )
    assert_file(
        ROOT / "tests" / "assembler" / "branch.oas",
        ROOT / "tests" / "assembler" / "branch.expected.hex",
        "hex",
    )
    assert_file(
        ROOT / "tests" / "assembler" / "base16t.oas",
        ROOT / "tests" / "assembler" / "base16t.expected.hex",
        "hex",
    )
    assert_error("MVI r64, 1\n", "register 64 out of range")
    with tempfile.NamedTemporaryFile("w", suffix=".oas", delete=False) as temp:
        temp.write("MVF r1, [0xfff]\nMVT r1, [0xfff]\nMSI [0xfff], 0x1234\n")
        high_addr_path = Path(temp.name)

    try:
        run_asm(high_addr_path, "hex")
    finally:
        high_addr_path.unlink()

    assert_error("MVT r1, [0x1000]\n", "memory address 4096 out of range")
    assert_error("LDR r1, [r56 + 32]\n", "off6 32 out of range")
    assert_program_image(
        ROOT / "examples" / "base16" / "add_store.oas",
        ROOT / "tests" / "assembler" / "add_store.expected.dap16",
        "dap16",
    )
    assert_program_image(
        ROOT / "examples" / "base16" / "add_store.oas",
        ROOT / "tests" / "assembler" / "add_store.expected.spi16",
        "spi16-hex",
    )
    print("assembler tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
