# OASIS Assembly

This page defines the assembly syntax used by OASIS v0.1 examples and
compliance tests.

## Syntax

- One instruction per line.
- Labels end with `:`.
- Comments begin with `;`.
- Registers are written as `r0` through `r63`.
- Decimal immediates are written as `42`.
- Binary immediates are written as `0b101010`.
- Hex immediates are written as `0x002a`.
- Memory operands use brackets, such as `[0x001]`.

## Example

```asm
start:
MVI r1, 0x000a
MVI r2, 0x0014
ADD r1, r2
MVT r1, [0x001]
JMP start
```

## Future Tooling

The next useful tool is a small assembler that emits OASIS 32-bit instruction
words for implementation test harnesses.
