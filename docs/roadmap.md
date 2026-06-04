# Roadmap

## Phase 1: Stabilize OASIS Base-16

- Define architectural state
- Define exact instruction encoding
- Define memory behavior
- Define reset behavior
- Define all current opcodes
- Define reserved bits and invalid encodings
- Publish machine-readable opcode tables

## Phase 2: Make The Spec Executable

- Add YAML compliance tests for every instruction
- Add a tiny assembler
- Add a Python reference emulator
- Generate instruction docs from opcode tables
- Validate duplicate opcodes in CI

## Phase 3: Support Implementations

- Provide compliance reports
- Document repo-to-repo dependency options
- Add a conformance badge such as `OASIS Base-16 Compliant`
- Add guides for building a minimal OASIS core

## Deferred

Do not add privilege modes, interrupts, exceptions, byte addressing, or new ALU
features until Base-16 v0.1 is specified and tested.
