# OASIS v0.2 Local Roadmap

This branch-local roadmap tracks v0.2 exploration before it is promoted into
the public roadmap and release notes.

## Architecture Goals

- Expand absolute data-memory operands from `addr9` to `addr12`.
- Preserve 32-bit instruction width while using idle memory-format bits.
- Keep Base-16T GCC/binutils compatibility green while evolving the ISA.
- Add compliance coverage before each v0.2 feature is considered stable.
- Define a documented expansion template for peripheral-oriented instructions.

## Toolchain Goals

- Keep GCC 14 and binutils building from source on Linux CI and Darwin.
- Improve compiler-facing memory behavior for globals, arrays, and stack data.
- Add targeted C smoke tests for larger data-memory addresses.
- Document any ABI/layout changes that affect implementation repositories.

## Candidate v0.2 Features

- Wider absolute data-memory addressing: 4096 words instead of 512 words.
- Peripheral instruction templates for GPIO, external memory controllers,
  timers, UART/SPI/I2C controllers, and implementation-defined control blocks.
- Wider program-counter paths or long-branch/call forms.
- Clear debug/halt/exit convention for bare-metal programs.
- Interrupt or exception entry/return convention.
- More complete freestanding C++ runtime hooks.

## Current Sprint

- Update memory encodings from `addr9` to `addr12`.
- Update assembler, generated docs, binutils opcode tables, GAS parsing, BFD
  relocations, and validation tests.
- Draft class `00` instruction-expansion guidance before assigning any new
  peripheral opcodes.
- Leave the archived v0.1 spec untouched and document v0.2 behavior in current
  tables/spec files.

## Instruction Expansion Notes

- Class `00` remains the preferred expansion class for implementation support
  instructions because Base-16 already reserves it and Base-16T uses it for
  compiler-facing mechanisms.
- Existing Base-16T class `00` opcodes must remain stable for v0.1 software:
  `ADI`, `SBI`, `LDR`, `STR`, `CALL`, `RET`, `JMR`, `JLT`, `JGE`, `JLTU`, and
  `JGEU`.
- Candidate class `00` opcode space for v0.2 exploration includes opcode
  `0000` and opcodes `1100` through `1111`.
- Peripheral instructions should prefer small, regular operand templates over
  device-specific one-off encodings.
- Memory-mapped IO remains the portable fallback. Dedicated peripheral
  instructions should be treated as optional profiles or implementation
  extensions until compliance tests and toolchain lowering are defined.
