# OASIS

OASIS is the Open Architecture Simplified Instruction Set: a small,
implementation-friendly ISA intended for learning, FPGA soft cores,
microcontrollers, and custom chip experiments.

This repository answers: "What must any correct OASIS CPU do?" Implementation
repositories, such as DungV, consume this contract and report compatibility
against a pinned OASIS version.

## Current Profile

OASIS v0.1-draft defines the Base-16 profile:

- 16-bit data path
- 32-bit instructions
- 64 general purpose registers
- Word-addressed data memory
- Basic ALU, move/immediate, load/store, and jump/branch operations
- No privilege modes, interrupts, exceptions, or status flags

Start with [spec/oasis-v0.1.md](spec/oasis-v0.1.md).

## Repository Layout

| Path | Purpose |
| ---- | ------- |
| `spec/` | Versioned ISA specification and topic pages |
| `instructions/` | Per-instruction reference pages |
| `tables/` | Machine-readable opcode and encoding tables |
| `tests/compliance/` | Shared ISA compliance test definitions |
| `tools/` | Documentation and table validation tools |
| `docs/` | Roadmap and process notes |

## Development Rule

Do not grow the ISA until OASIS Base-16 v0.1 has complete instruction docs,
machine-readable opcode tables, and compliance tests that implementation repos
can run.
