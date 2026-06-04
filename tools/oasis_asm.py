#!/usr/bin/env python3
"""OASIS Base-16 assembler.

The assembler emits one 32-bit instruction per source instruction. The default
output format is a `$readmemb`-friendly text file with one binary instruction per
line.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import struct
import sys


XLEN = 16
REG_COUNT = 64
DATA_ADDR_MAX = 0x1FF
PC_MAX = 0xFF
IMM16_MAX = 0xFFFF
IMM6_MAX = 0x3F
OFF6_MIN = -32
OFF6_MAX = 31

CLASS_TOOL = 0b00
CLASS_ALU = 0b01
CLASS_REG = 0b10
CLASS_MEM = 0b11

TOOL_OPS = {
    "ADI": 0b0001,
    "SBI": 0b0010,
    "LDR": 0b0011,
    "STR": 0b0100,
    "CALL": 0b0101,
    "RET": 0b0110,
    "JMR": 0b0111,
    "JLT": 0b1000,
    "JGE": 0b1001,
    "JLTU": 0b1010,
    "JGEU": 0b1011,
}

ALU_OPS = {
    "ADD": 0b0001,
    "SUB": 0b0010,
    "AND": 0b0011,
    "OOR": 0b0100,
    "XOR": 0b0101,
    "SHR": 0b0110,
    "SHL": 0b0111,
    "RTR": 0b1000,
    "RTL": 0b1001,
    "NOT": 0b1010,
    "MLT": 0b1011,
    "JEQ": 0b1100,
    "JNE": 0b1101,
    "JMP": 0b1110,
    "NOP": 0b1111,
}

REG_OPS = {
    "MVV": 0b10,
    "MVI": 0b11,
}

MEM_OPS = {
    "MVF": 0b01,
    "MVT": 0b10,
    "MSI": 0b11,
}


@dataclass(frozen=True)
class SourceLine:
    path: Path
    line_no: int
    text: str


class AssemblerError(Exception):
    pass


def strip_comment(line: str) -> str:
    return line.split(";", 1)[0].strip()


def split_operands(text: str) -> list[str]:
    if not text:
        return []
    return [operand.strip() for operand in text.split(",") if operand.strip()]


def parse_int(token: str, labels: dict[str, int], line: SourceLine) -> int:
    token = token.strip()
    if token in labels:
        return labels[token]
    try:
        return int(token, 0)
    except ValueError as exc:
        raise AssemblerError(f"{line.path}:{line.line_no}: unknown value {token!r}") from exc


def require_range(value: int, low: int, high: int, what: str, line: SourceLine) -> int:
    if value < low or value > high:
        raise AssemblerError(
            f"{line.path}:{line.line_no}: {what} {value} out of range {low}..{high}"
        )
    return value


def parse_register(token: str, line: SourceLine) -> int:
    match = re.fullmatch(r"[rR]([0-9]+)", token.strip())
    if not match:
        raise AssemblerError(f"{line.path}:{line.line_no}: expected register, got {token!r}")
    return require_range(int(match.group(1)), 0, REG_COUNT - 1, "register", line)


def parse_mem_addr(token: str, labels: dict[str, int], line: SourceLine) -> int:
    match = re.fullmatch(r"\[(.+)\]", token.strip())
    if not match:
        raise AssemblerError(f"{line.path}:{line.line_no}: expected memory address, got {token!r}")
    value = parse_int(match.group(1).strip(), labels, line)
    return require_range(value, 0, DATA_ADDR_MAX, "memory address", line)


def parse_mem_ref(token: str, labels: dict[str, int], line: SourceLine) -> tuple[int, int]:
    match = re.fullmatch(
        r"\[\s*([rR][0-9]+)(?:\s*([+-])\s*([A-Za-z_][A-Za-z0-9_]*|0x[0-9A-Fa-f]+|0b[01]+|[0-9]+))?\s*\]",
        token.strip(),
    )
    if not match:
        raise AssemblerError(
            f"{line.path}:{line.line_no}: expected register memory reference, got {token!r}"
        )

    base = parse_register(match.group(1), line)
    offset = 0
    if match.group(3) is not None:
        offset = parse_int(match.group(3), labels, line)
        if match.group(2) == "-":
            offset = -offset

    require_range(offset, OFF6_MIN, OFF6_MAX, "off6", line)
    return base, offset & IMM6_MAX


def normalize_source(path: Path) -> list[SourceLine]:
    source_lines: list[SourceLine] = []
    for line_no, raw_line in enumerate(path.read_text().splitlines(), start=1):
        line = strip_comment(raw_line)
        if line:
            source_lines.append(SourceLine(path, line_no, line))
    return source_lines


def collect_labels(lines: list[SourceLine]) -> tuple[dict[str, int], list[SourceLine]]:
    labels: dict[str, int] = {}
    instructions: list[SourceLine] = []
    pc = 0

    for line in lines:
        text = line.text
        while ":" in text:
            label, rest = text.split(":", 1)
            label = label.strip()
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", label):
                raise AssemblerError(f"{line.path}:{line.line_no}: invalid label {label!r}")
            if label in labels:
                raise AssemblerError(f"{line.path}:{line.line_no}: duplicate label {label!r}")
            labels[label] = pc
            text = rest.strip()
            if not text:
                break
        if text:
            instructions.append(SourceLine(line.path, line.line_no, text))
            pc = require_range(pc + 1, 0, PC_MAX + 1, "program length", line)

    return labels, instructions


def parse_instruction(line: SourceLine) -> tuple[str, list[str]]:
    parts = line.text.split(None, 1)
    mnemonic = parts[0].upper()
    operands = split_operands(parts[1] if len(parts) > 1 else "")
    return mnemonic, operands


def expect_count(operands: list[str], count: int, mnemonic: str, line: SourceLine) -> None:
    if len(operands) != count:
        raise AssemblerError(
            f"{line.path}:{line.line_no}: {mnemonic} expects {count} operand(s), "
            f"got {len(operands)}"
        )


def encode_alu(mnemonic: str, operands: list[str], labels: dict[str, int], line: SourceLine) -> int:
    opcode = ALU_OPS[mnemonic]
    ra = 0
    rb_or_imm6 = 0
    target = 0

    if mnemonic in {"ADD", "SUB", "AND", "OOR", "XOR", "MLT"}:
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb_or_imm6 = parse_register(operands[1], line)
    elif mnemonic in {"SHR", "SHL", "RTR", "RTL"}:
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb_or_imm6 = require_range(parse_int(operands[1], labels, line), 0, IMM6_MAX, "imm6", line)
    elif mnemonic == "NOT":
        expect_count(operands, 1, mnemonic, line)
        ra = parse_register(operands[0], line)
    elif mnemonic in {"JEQ", "JNE"}:
        expect_count(operands, 3, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb_or_imm6 = parse_register(operands[1], line)
        target = require_range(parse_int(operands[2], labels, line), 0, PC_MAX, "target8", line)
    elif mnemonic == "JMP":
        expect_count(operands, 1, mnemonic, line)
        target = require_range(parse_int(operands[0], labels, line), 0, PC_MAX, "target8", line)
    elif mnemonic == "NOP":
        expect_count(operands, 0, mnemonic, line)
    else:
        raise AssemblerError(f"{line.path}:{line.line_no}: unsupported ALU op {mnemonic}")

    return (
        (CLASS_ALU << 30)
        | (opcode << 26)
        | (ra << 20)
        | (rb_or_imm6 << 14)
        | (target << 6)
    )


def encode_tool(mnemonic: str, operands: list[str], labels: dict[str, int], line: SourceLine) -> int:
    opcode = TOOL_OPS[mnemonic]
    ra = 0
    rb = 0
    off6 = 0
    target = 0
    imm16 = 0

    if mnemonic in {"ADI", "SBI"}:
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        imm16 = require_range(parse_int(operands[1], labels, line), 0, IMM16_MAX, "imm16", line)
        return (CLASS_TOOL << 30) | (opcode << 26) | (ra << 20) | imm16

    if mnemonic in {"LDR", "STR"}:
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb, off6 = parse_mem_ref(operands[1], labels, line)
        return (CLASS_TOOL << 30) | (opcode << 26) | (ra << 20) | (rb << 14) | (off6 << 8)

    if mnemonic == "CALL":
        expect_count(operands, 1, mnemonic, line)
        target = require_range(parse_int(operands[0], labels, line), 0, PC_MAX, "target8", line)
        return (CLASS_TOOL << 30) | (opcode << 26) | (target << 6)

    if mnemonic == "RET":
        expect_count(operands, 0, mnemonic, line)
        return (CLASS_TOOL << 30) | (opcode << 26)

    if mnemonic == "JMR":
        expect_count(operands, 1, mnemonic, line)
        rb = parse_register(operands[0], line)
        return (CLASS_TOOL << 30) | (opcode << 26) | (rb << 14)

    if mnemonic in {"JLT", "JGE", "JLTU", "JGEU"}:
        expect_count(operands, 3, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb = parse_register(operands[1], line)
        target = require_range(parse_int(operands[2], labels, line), 0, PC_MAX, "target8", line)
        return (CLASS_TOOL << 30) | (opcode << 26) | (ra << 20) | (rb << 14) | (target << 6)

    raise AssemblerError(f"{line.path}:{line.line_no}: unsupported toolchain op {mnemonic}")


def encode_register(
    mnemonic: str,
    operands: list[str],
    labels: dict[str, int],
    line: SourceLine,
) -> int:
    opcode = REG_OPS[mnemonic]
    ra = 0
    rb = 0
    imm16 = 0

    if mnemonic == "MVV":
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        rb = parse_register(operands[1], line)
    elif mnemonic == "MVI":
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        imm16 = require_range(parse_int(operands[1], labels, line), 0, IMM16_MAX, "imm16", line)

    return (CLASS_REG << 30) | (opcode << 28) | (ra << 22) | (rb << 16) | imm16


def encode_memory(
    mnemonic: str,
    operands: list[str],
    labels: dict[str, int],
    line: SourceLine,
) -> int:
    opcode = MEM_OPS[mnemonic]

    if mnemonic in {"MVF", "MVT"}:
        expect_count(operands, 2, mnemonic, line)
        ra = parse_register(operands[0], line)
        addr = parse_mem_addr(operands[1], labels, line)
        return (CLASS_MEM << 30) | (opcode << 28) | (ra << 22) | (addr << 13)

    if mnemonic == "MSI":
        expect_count(operands, 2, mnemonic, line)
        addr = parse_mem_addr(operands[0], labels, line)
        imm16 = require_range(parse_int(operands[1], labels, line), 0, IMM16_MAX, "imm16", line)
        return (CLASS_MEM << 30) | (opcode << 28) | (addr << 19) | imm16

    raise AssemblerError(f"{line.path}:{line.line_no}: unsupported memory op {mnemonic}")


def assemble(path: Path) -> list[int]:
    labels, instructions = collect_labels(normalize_source(path))
    words: list[int] = []

    for line in instructions:
        mnemonic, operands = parse_instruction(line)
        if mnemonic in TOOL_OPS:
            words.append(encode_tool(mnemonic, operands, labels, line))
        elif mnemonic in ALU_OPS:
            words.append(encode_alu(mnemonic, operands, labels, line))
        elif mnemonic in REG_OPS:
            words.append(encode_register(mnemonic, operands, labels, line))
        elif mnemonic in MEM_OPS:
            words.append(encode_memory(mnemonic, operands, labels, line))
        else:
            raise AssemblerError(f"{line.path}:{line.line_no}: unknown instruction {mnemonic!r}")

    return words


def format_words(words: list[int], output_format: str) -> bytes:
    if output_format == "binstr":
        return "".join(f"{word:032b}\n" for word in words).encode()
    if output_format == "hex":
        return "".join(f"{word:08x}\n" for word in words).encode()
    if output_format == "raw-be":
        return b"".join(struct.pack(">I", word) for word in words)
    if output_format == "raw-le":
        return b"".join(struct.pack("<I", word) for word in words)
    raise ValueError(output_format)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble OASIS Base-16 source")
    parser.add_argument("input", type=Path, help="input .oas assembly file")
    parser.add_argument("-o", "--output", type=Path, help="output file")
    parser.add_argument(
        "-f",
        "--format",
        choices=["binstr", "hex", "raw-be", "raw-le"],
        default="binstr",
        help="output format; default is binstr for Verilog $readmemb",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        words = assemble(args.input)
        output = format_words(words, args.format)
    except AssemblerError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.output:
        args.output.write_bytes(output)
    else:
        sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
