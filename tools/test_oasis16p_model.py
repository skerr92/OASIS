#!/usr/bin/env python3
"""Behavioral compliance tests for the executable OASIS-16P model."""

from oasis16p_model import (
    CAUSE_ILLEGAL_INSTRUCTION,
    CAUSE_PRIVILEGE_VIOLATION,
    CAUSE_SOFTWARE_TRAP,
    CSR_IENABLE,
    CSR_SCRATCH,
    CSR_STATUS,
    CSR_SYSINFO,
    INTERRUPT_FLAG,
    STATUS_IE,
    STATUS_MODE,
    STATUS_PIE,
    STATUS_PMODE,
    STATUS_WFI,
    Oasis16PModel,
    encode_system,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    model = Oasis16PModel(tvec=0x40)
    require(model.status == STATUS_MODE, "reset must enter Machine mode with IE clear")

    model.status = STATUS_IE  # User mode with interrupts enabled.
    result = model.execute_system(encode_system(0, arg8=0x2A), pc=0x10)
    require((result.action, result.pc) == ("trap", 0x40), "TRAP must redirect")
    require(model.epc == 0x11 and model.cause == CAUSE_SOFTWARE_TRAP, "TRAP state")
    require(model.tval == 0x2A, "TRAP immediate must reach TVAL")
    require(model.status == (STATUS_MODE | STATUS_PIE), "TRAP saved state")

    result = model.execute_system(encode_system(1), pc=0x40)
    require((result.action, result.pc) == ("eret", 0x11), "ERET return PC")
    require(model.status == STATUS_IE, "ERET must restore User mode and IE")

    model.status = STATUS_MODE | STATUS_IE
    model.ienable = 0xFFFF
    model.set_pending((1 << 7) | (1 << 2) | (1 << 12))
    result = model.take_interrupt(next_pc=0x22)
    require(result is not None and result.pc == 0x40, "eligible interrupt must redirect")
    require(model.cause == (INTERRUPT_FLAG | 2), "lowest interrupt ID wins")
    require(model.epc == 0x22 and model.tval == 0, "interrupt state")
    require(model.status == (STATUS_MODE | STATUS_PMODE | STATUS_PIE), "IRQ save state")

    model = Oasis16PModel(tvec=0x40)
    result = model.execute_system(encode_system(2), pc=3)
    require(result.action == "wait" and model.status & STATUS_WFI, "WFI enters wait")
    model.set_pending(1 << 4)
    require(not model.waiting and not model.status & STATUS_WFI, "masked pending IRQ wakes WFI")
    require(model.take_interrupt(4) is None, "masked IRQ must not trap")
    result = model.execute_system(encode_system(2), pc=4)
    require(result.action == "retire" and not model.waiting, "pending IRQ prevents wait")

    model.execute_system(encode_system(4, ra=5, arg8=CSR_IENABLE), 4, 0x00F0)
    require(model.ienable == 0x00F0, "CSRW")
    model.execute_system(encode_system(5, ra=5, arg8=CSR_IENABLE), 5, 0x0003)
    require(model.ienable == 0x00F3, "CSRS")
    model.execute_system(encode_system(6, ra=5, arg8=CSR_IENABLE), 6, 0x0030)
    require(model.ienable == 0x00C3, "CSRC")
    read = model.execute_system(encode_system(3, ra=9, arg8=CSR_IENABLE), 7)
    require(read.register_write == (9, 0x00C3), "CSRR")

    model.status = 0
    read = model.execute_system(encode_system(3, ra=1, arg8=CSR_SYSINFO), 8)
    require(read.register_write == (1, 1), "User SYSINFO read")
    fault_word = encode_system(4, ra=1, arg8=CSR_SCRATCH)
    result = model.execute_system(fault_word, 9, 0x1234)
    require(result.action == "trap" and model.cause == CAUSE_PRIVILEGE_VIOLATION, "privilege trap")
    require(model.epc == 9 and model.tval == fault_word & 0xFFFF, "privilege fault state")

    malformed = encode_system(0, ra=1, arg8=3)
    model.execute_system(malformed, 0x20)
    require(model.cause == CAUSE_ILLEGAL_INSTRUCTION and model.epc == 0x20, "reserved-bit trap")

    model.raise_exception(0x06, 0x8123, 0x33)
    require(model.epc == 0x33 and model.tval == 0x8123, "MMIO fault TVAL")

    print("OASIS-16P executable model tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
