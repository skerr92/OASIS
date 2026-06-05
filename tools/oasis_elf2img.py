#!/usr/bin/env python3
"""Convert OASIS ELF files into programming images."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import struct
import sys

import oasis_asm
import oasis_program_image


ELF_MAGIC = b"\x7fELF"
ELFCLASS32 = 1
ELFDATA2LSB = 1
ET_EXEC = 2
ET_REL = 1
EM_OASIS16 = 0x4F16
SHT_PROGBITS = 1
SHF_ALLOC = 0x2
SHF_EXECINSTR = 0x4
PT_LOAD = 1
PF_X = 0x1


@dataclass(frozen=True)
class ElfHeader:
    e_type: int
    e_machine: int
    e_phoff: int
    e_shoff: int
    e_phentsize: int
    e_phnum: int
    e_shentsize: int
    e_shnum: int
    e_shstrndx: int


@dataclass(frozen=True)
class ProgramHeader:
    p_type: int
    p_offset: int
    p_vaddr: int
    p_filesz: int
    p_flags: int


@dataclass(frozen=True)
class SectionHeader:
    name_offset: int
    name: str
    sh_type: int
    sh_flags: int
    sh_addr: int
    sh_offset: int
    sh_size: int


class ElfError(Exception):
    pass


def require_range(data: bytes, offset: int, size: int, what: str) -> None:
    if offset < 0 or size < 0 or offset + size > len(data):
        raise ElfError(f"{what} extends beyond end of file")


def read_c_string(data: bytes, offset: int) -> str:
    if offset < 0 or offset >= len(data):
        return ""
    end = data.find(b"\0", offset)
    if end < 0:
        end = len(data)
    return data[offset:end].decode("ascii", errors="replace")


def parse_header(data: bytes) -> ElfHeader:
    require_range(data, 0, 52, "ELF header")
    if data[:4] != ELF_MAGIC:
        raise ElfError("input is not an ELF file")
    if data[4] != ELFCLASS32:
        raise ElfError("only ELF32 is supported")
    if data[5] != ELFDATA2LSB:
        raise ElfError("only little-endian ELF is supported")

    fields = struct.unpack_from("<HHIIIIIHHHHHH", data, 16)
    header = ElfHeader(
        e_type=fields[0],
        e_machine=fields[1],
        e_phoff=fields[4],
        e_shoff=fields[5],
        e_phentsize=fields[8],
        e_phnum=fields[9],
        e_shentsize=fields[10],
        e_shnum=fields[11],
        e_shstrndx=fields[12],
    )

    if header.e_machine != EM_OASIS16:
        raise ElfError(f"unsupported ELF machine 0x{header.e_machine:04x}")
    if header.e_type not in {ET_EXEC, ET_REL}:
        raise ElfError(f"unsupported ELF type {header.e_type}")
    return header


def parse_program_headers(data: bytes, header: ElfHeader) -> list[ProgramHeader]:
    headers: list[ProgramHeader] = []
    if header.e_phoff == 0 or header.e_phnum == 0:
        return headers
    if header.e_phentsize < 32:
        raise ElfError("program header entry is too small")

    require_range(data, header.e_phoff, header.e_phentsize * header.e_phnum, "program headers")
    for index in range(header.e_phnum):
        offset = header.e_phoff + index * header.e_phentsize
        fields = struct.unpack_from("<IIIIIIII", data, offset)
        headers.append(
            ProgramHeader(
                p_type=fields[0],
                p_offset=fields[1],
                p_vaddr=fields[2],
                p_filesz=fields[4],
                p_flags=fields[6],
            )
        )
    return headers


def parse_section_headers(data: bytes, header: ElfHeader) -> list[SectionHeader]:
    if header.e_shoff == 0 or header.e_shnum == 0:
        return []
    if header.e_shentsize < 40:
        raise ElfError("section header entry is too small")

    require_range(data, header.e_shoff, header.e_shentsize * header.e_shnum, "section headers")
    raw_headers: list[tuple[int, int, int, int, int, int]] = []
    for index in range(header.e_shnum):
        offset = header.e_shoff + index * header.e_shentsize
        fields = struct.unpack_from("<IIIIIIIIII", data, offset)
        raw_headers.append((fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]))

    shstr = b""
    if 0 <= header.e_shstrndx < len(raw_headers):
        _, _, _, _, sh_offset, sh_size = raw_headers[header.e_shstrndx]
        require_range(data, sh_offset, sh_size, "section string table")
        shstr = data[sh_offset : sh_offset + sh_size]

    sections: list[SectionHeader] = []
    for name_offset, sh_type, sh_flags, sh_addr, sh_offset, sh_size in raw_headers:
        sections.append(
            SectionHeader(
                name_offset=name_offset,
                name=read_c_string(shstr, name_offset) if shstr else "",
                sh_type=sh_type,
                sh_flags=sh_flags,
                sh_addr=sh_addr,
                sh_offset=sh_offset,
                sh_size=sh_size,
            )
        )
    return sections


def words_from_bytes(blob: bytes) -> list[int]:
    if len(blob) % 4 != 0:
        raise ElfError("instruction payload size is not a multiple of 4 bytes")
    return [struct.unpack_from("<I", blob, offset)[0] for offset in range(0, len(blob), 4)]


def extract_text(data: bytes, section_name: str) -> tuple[list[int], int]:
    header = parse_header(data)

    load_segments = [
        ph
        for ph in parse_program_headers(data, header)
        if ph.p_type == PT_LOAD and (ph.p_flags & PF_X) and ph.p_filesz > 0
    ]
    if load_segments:
        segment = min(load_segments, key=lambda ph: ph.p_vaddr)
        require_range(data, segment.p_offset, segment.p_filesz, "executable LOAD segment")
        return words_from_bytes(data[segment.p_offset : segment.p_offset + segment.p_filesz]), segment.p_vaddr

    sections = parse_section_headers(data, header)
    named = [section for section in sections if section.name == section_name]
    executable = [
        section
        for section in sections
        if section.sh_type == SHT_PROGBITS
        and (section.sh_flags & SHF_ALLOC)
        and (section.sh_flags & SHF_EXECINSTR)
        and section.sh_size > 0
    ]
    candidates = named or executable
    if not candidates:
        raise ElfError(f"could not find {section_name!r} or executable section")

    section = candidates[0]
    require_range(data, section.sh_offset, section.sh_size, f"{section.name or 'text'} section")
    return words_from_bytes(data[section.sh_offset : section.sh_offset + section.sh_size]), section.sh_addr


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="input OASIS ELF file")
    parser.add_argument("-o", "--output", type=Path, help="output file")
    parser.add_argument(
        "-f",
        "--format",
        choices=["dap16", "spi16-hex", "hex", "binstr"],
        default="dap16",
        help="output format",
    )
    parser.add_argument(
        "--start",
        type=lambda value: int(value, 0),
        help="override instruction memory start address",
    )
    parser.add_argument(
        "--section",
        default=".text",
        help="section to extract when no executable LOAD segment exists",
    )
    return parser.parse_args(argv)


def format_words(words: list[int], output_format: str, start: int) -> str:
    if output_format == "dap16":
        return oasis_program_image.dap16_script(words, start)
    if output_format == "spi16-hex":
        return oasis_program_image.spi16_hex(words, start)
    if output_format == "hex":
        return "".join(f"{word:08x}\n" for word in words)
    if output_format == "binstr":
        return "".join(f"{word:032b}\n" for word in words)
    raise ValueError(output_format)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        words, detected_start = extract_text(args.input.read_bytes(), args.section)
    except (OSError, ElfError) as exc:
        print(exc, file=sys.stderr)
        return 1

    start = args.start if args.start is not None else detected_start
    if start < 0 or start > oasis_asm.PC_MAX:
        print(f"start address {start} out of range 0..{oasis_asm.PC_MAX}", file=sys.stderr)
        return 1
    if start + len(words) > oasis_asm.PC_MAX + 1:
        print("program image exceeds instruction memory", file=sys.stderr)
        return 1

    output = format_words(words, args.format, start)
    if args.output:
        args.output.write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
