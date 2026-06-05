#!/usr/bin/env python3
"""Validate OASIS GCC backend and runtime skeleton consistency."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
GCC = ROOT / "toolchain" / "gcc14" / "backend" / "gcc" / "config" / "oasis16"
LIBGCC = ROOT / "toolchain" / "gcc14" / "backend" / "libgcc"
RUNTIME = ROOT / "toolchain" / "runtime"


def require(text: str, token: str, errors: list[str], where: str) -> None:
    if token not in text:
        errors.append(f"{where} missing {token}")


def main() -> int:
    errors: list[str] = []

    oasis_cc = (GCC / "oasis16.cc").read_text()
    oasis_h = (GCC / "oasis16.h").read_text()
    oasis_md = (GCC / "oasis16.md").read_text()
    constraints = (GCC / "constraints.md").read_text()
    predicates = (GCC / "predicates.md").read_text()
    protos = (GCC / "oasis16-protos.h").read_text()

    for token in [
        "TARGET_FUNCTION_ARG",
        "TARGET_FUNCTION_ARG_ADVANCE",
        "TARGET_FUNCTION_VALUE",
        "TARGET_LIBCALL_VALUE",
        "TARGET_RETURN_IN_MEMORY",
        "TARGET_LRA_P",
        "TARGET_LEGITIMATE_ADDRESS_P",
        "oasis16_expand_prologue",
        "oasis16_expand_epilogue",
        "oasis16_save_reg_p",
        "oasis16_saved_reg_count",
    ]:
        require(oasis_cc, token, errors, "oasis16.cc")

    for token in [
        "OASIS16_STACK_POINTER_REGNUM 56",
        "OASIS16_FRAME_POINTER_REGNUM 57",
        "OASIS16_RETURN_ADDRESS_REGNUM 58",
        "CALL_USED_REGISTERS",
        "REGNO_OK_FOR_BASE_P",
        "INITIAL_ELIMINATION_OFFSET",
        "RETURN_ADDR_RTX",
        "EPILOGUE_USES",
    ]:
        require(oasis_h, token, errors, "oasis16.h")

    for token in [
        '(define_expand "prologue"',
        '(define_expand "epilogue"',
        '(define_expand "call"',
        '(define_insn "*call"',
        '(define_insn "*call_no_clobber"',
        '(define_expand "call_value"',
        '(define_insn "*call_value"',
        '(define_insn "*call_value_no_clobber"',
        '(parallel [(call',
        '(parallel [(set',
        'match_operand:HI 0 "oasis16_call_address_operand" "S"',
        'match_operand:HI 1 "oasis16_call_address_operand" "S"',
        "(clobber (reg:HI R58))",
        '"r,I,S,m,r"',
        'match_operator 0 "comparison_operator"',
        "LDR %0, %1",
        "STR %1, %0",
    ]:
        require(oasis_md, token, errors, "oasis16.md")

    for token in [
        'define_constraint "S"',
        "symbol_ref",
        "label_ref",
    ]:
        require(constraints, token, errors, "constraints.md")

    for token in [
        'define_predicate "oasis16_call_operand"',
        'define_predicate "oasis16_call_address_operand"',
        "SYMBOL_REF_P(XEXP(op, 0))",
    ]:
        require(predicates, token, errors, "predicates.md")

    for token in [
        "oasis16_initial_elimination_offset",
        "oasis16_legitimate_address_p",
        "oasis16_return_addr_rtx",
    ]:
        require(protos, token, errors, "oasis16-protos.h")

    required_files = [
        RUNTIME / "crt0.S",
        RUNTIME / "crt0.oas",
        RUNTIME / "include" / "oasis.h",
        RUNTIME / "linker" / "oasis16.ld",
        RUNTIME / "libgcc" / "oasis16-libgcc.S",
        LIBGCC / "config" / "oasis16" / "lib1funcs.S",
        LIBGCC / "config" / "oasis16" / "t-oasis16",
        LIBGCC / "config.host.fragment",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"missing runtime/libgcc file: {path}")

    libgcc = (RUNTIME / "libgcc" / "oasis16-libgcc.S").read_text()
    for symbol in [
        "__mulhi3",
        "__ashlhi3",
        "__lshrhi3",
        "__udivhi3",
        "__umodhi3",
        "__divhi3",
        "__modhi3",
    ]:
        require(libgcc, symbol, errors, "oasis16-libgcc.S")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("validated GCC backend, ABI hooks, and runtime files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
