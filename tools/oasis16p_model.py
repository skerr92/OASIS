#!/usr/bin/env python3
"""Executable reference model for the OASIS-16P architectural state block."""

from __future__ import annotations

from dataclasses import dataclass


STATUS_IE = 1 << 0
STATUS_PIE = 1 << 1
STATUS_MODE = 1 << 2
STATUS_PMODE = 1 << 3
STATUS_WFI = 1 << 4
STATUS_WRITABLE = STATUS_IE | STATUS_PIE | STATUS_MODE | STATUS_PMODE

CSR_STATUS = 0x00
CSR_TVEC = 0x01
CSR_EPC = 0x02
CSR_CAUSE = 0x03
CSR_TVAL = 0x04
CSR_IENABLE = 0x05
CSR_IPENDING = 0x06
CSR_SCRATCH = 0x07
CSR_SYSINFO = 0x08

CAUSE_ILLEGAL_INSTRUCTION = 0x01
CAUSE_PRIVILEGE_VIOLATION = 0x02
CAUSE_SOFTWARE_TRAP = 0x08
INTERRUPT_FLAG = 0x8000

SYSTEM_OPCODE = 0xE


@dataclass
class StepResult:
    action: str
    pc: int
    register_write: tuple[int, int] | None = None


@dataclass
class Oasis16PModel:
    """State-only model; the surrounding core owns GPRs, retirement, and memory."""

    status: int = STATUS_MODE
    tvec: int = 0
    epc: int = 0
    cause: int = 0
    tval: int = 0
    ienable: int = 0
    ipending: int = 0
    scratch: int = 0
    sysinfo: int = 1
    waiting: bool = False
    def __post_init__(self) -> None:
        self._sync_status()

    @property
    def machine_mode(self) -> bool:
        return bool(self.status & STATUS_MODE)

    def _sync_status(self) -> None:
        self.status &= STATUS_WRITABLE
        if self.waiting:
            self.status |= STATUS_WFI

    def set_pending(self, pending: int) -> None:
        self.ipending = pending & 0xFFFF
        if self.ipending:
            self.waiting = False
        self._sync_status()

    def _enter_trap(self, epc: int, cause: int, tval: int) -> StepResult:
        prior_ie = bool(self.status & STATUS_IE)
        prior_mode = bool(self.status & STATUS_MODE)
        self.epc = epc & 0xFF
        self.cause = cause & 0xFFFF
        self.tval = tval & 0xFFFF
        self.status &= ~(STATUS_IE | STATUS_PIE | STATUS_MODE | STATUS_PMODE)
        if prior_ie:
            self.status |= STATUS_PIE
        if prior_mode:
            self.status |= STATUS_PMODE
        self.status |= STATUS_MODE
        self.waiting = False
        self._sync_status()
        return StepResult("trap", self.tvec & 0xFF)

    def raise_exception(self, cause: int, tval: int, fault_pc: int) -> StepResult:
        return self._enter_trap(fault_pc, cause, tval)

    def take_interrupt(self, next_pc: int) -> StepResult | None:
        eligible = self.ipending & self.ienable
        if not (self.status & STATUS_IE) or not eligible:
            return None
        source = (eligible & -eligible).bit_length() - 1
        return self._enter_trap(next_pc, INTERRUPT_FLAG | source, 0)

    def _read_csr(self, csr: int) -> int | None:
        values = {
            CSR_STATUS: self.status,
            CSR_TVEC: self.tvec,
            CSR_EPC: self.epc,
            CSR_CAUSE: self.cause,
            CSR_TVAL: self.tval,
            CSR_IENABLE: self.ienable,
            CSR_IPENDING: self.ipending,
            CSR_SCRATCH: self.scratch,
            CSR_SYSINFO: self.sysinfo,
        }
        return values.get(csr)

    def _write_csr(self, csr: int, value: int) -> bool:
        value &= 0xFFFF
        if csr == CSR_STATUS:
            self.status = value & STATUS_WRITABLE
            self._sync_status()
        elif csr == CSR_TVEC:
            self.tvec = value & 0xFF
        elif csr == CSR_EPC:
            self.epc = value & 0xFF
        elif csr == CSR_IENABLE:
            self.ienable = value
        elif csr == CSR_SCRATCH:
            self.scratch = value
        else:
            return False
        return True

    def execute_system(self, word: int, pc: int, ra_value: int = 0) -> StepResult:
        next_pc = (pc + 1) & 0xFF
        if ((word >> 30) & 0x3) != 0 or ((word >> 26) & 0xF) != SYSTEM_OPCODE:
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)

        subop = (word >> 22) & 0xF
        ra = (word >> 16) & 0x3F
        arg8 = (word >> 8) & 0xFF
        low8 = word & 0xFF

        if subop == 0:
            if ra or low8:
                return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)
            return self._enter_trap(next_pc, CAUSE_SOFTWARE_TRAP, arg8)

        if subop in {1, 2} and (ra or arg8 or low8):
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)
        if subop in {3, 4, 5, 6} and low8:
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)
        if subop > 6:
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)

        if subop == 1:
            if not self.machine_mode:
                return self.raise_exception(CAUSE_PRIVILEGE_VIOLATION, word, pc)
            return_pc = self.epc
            prior_ie = bool(self.status & STATUS_PIE)
            prior_mode = bool(self.status & STATUS_PMODE)
            self.status &= ~(STATUS_IE | STATUS_PIE | STATUS_MODE | STATUS_PMODE)
            if prior_ie:
                self.status |= STATUS_IE
            if prior_mode:
                self.status |= STATUS_MODE
            self._sync_status()
            return StepResult("eret", return_pc)

        if subop == 2:
            if not self.machine_mode:
                return self.raise_exception(CAUSE_PRIVILEGE_VIOLATION, word, pc)
            self.waiting = self.ipending == 0
            self._sync_status()
            return StepResult("wait" if self.waiting else "retire", next_pc)

        value = self._read_csr(arg8)
        if value is None:
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)
        if not self.machine_mode and arg8 != CSR_SYSINFO:
            return self.raise_exception(CAUSE_PRIVILEGE_VIOLATION, word, pc)

        if subop == 3:
            return StepResult("retire", next_pc, (ra, value))
        if not self.machine_mode or arg8 in {CSR_CAUSE, CSR_TVAL, CSR_IPENDING, CSR_SYSINFO}:
            return self.raise_exception(CAUSE_PRIVILEGE_VIOLATION, word, pc)
        new_value = ra_value
        if subop == 5:
            new_value = value | ra_value
        elif subop == 6:
            new_value = value & ~ra_value
        if not self._write_csr(arg8, new_value):
            return self.raise_exception(CAUSE_ILLEGAL_INSTRUCTION, word, pc)
        return StepResult("retire", next_pc)


def encode_system(subop: int, ra: int = 0, arg8: int = 0) -> int:
    return (SYSTEM_OPCODE << 26) | (subop << 22) | (ra << 16) | (arg8 << 8)
