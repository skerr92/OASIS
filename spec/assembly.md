# OASIS Assembly

This page defines the assembly syntax used by OASIS v1.0 examples and
compliance tests.

## Syntax

- One instruction per line.
- Labels end with `:`.
- Comments begin with `;`.
- Registers are written as `r0` through `r63`; Base-16T also defines `sap`
  (`r59`) and `sdata` (`r60`).
- Decimal immediates are written as `42`.
- Binary immediates are written as `0b101010`.
- Hex immediates are written as `0x002a`.
- Direct operands explicitly use `mem:[addr11]` or `io:[addr11]`.
- Far pointer literals use `mem:addr15` or `io:addr15`, such as
  `MVI sap, io:0x0100`.
- Base-16T register-relative memory operands use `[rN]`, `[rN + off6]`, or `[rN - off6]`.

## Example

```asm
start:
MVI r1, 0x000a
MVI r2, 0x0014
ADD r1, r2
MVT r1, mem:[0x001]
JMP start
```

Base-16T example:

```asm
SBI r56, 1
STR r4, [r56 + 0]
CALL function
RET
```

Scratch-staged far/MMIO write:

```asm
MVI sap, io:0x0100
MSI mem:[0x0000], 0x1234
MCP [sap], mem:[0x0000]
```

## Tooling

The dependency-free assembler lives at `tools/oasis_asm.py` and is wrapped by
`bin/oasis-asm`. It emits OASIS 32-bit instruction words for examples,
compliance fixtures, and implementation test harnesses.

See [../docs/assembler.md](../docs/assembler.md).
