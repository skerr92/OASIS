# External Memory Control

Status: v0.2 design note.

OASIS Base-16T is a word-addressed 16-bit profile. The base architectural data
memory is 4096 words in the current v0.2 draft tables, but implementations may
attach larger or slower storage through an external memory controller.

This document describes the expected contract for such controllers without
assigning new mandatory instructions.

## Design Goals

- Preserve Base-16/Base-16T software compatibility.
- Keep memory-mapped IO as the portable baseline.
- Allow FPGA soft cores to attach SRAM, PSRAM, SDRAM, HyperRAM, or board-local
  memory without changing the core ISA.
- Give C/C++ toolchains enough linker/runtime information to place heap, stack,
  globals, or buffers in external memory.
- Leave room for optional controller-specific extensions later.

## Addressing Model

Base-16T software sees 16-bit word addresses for data memory. External memory
controllers should expose one or more windows inside that address space.

Recommended model:

| Concept | Description |
| ------- | ----------- |
| Window base | First OASIS data-memory word mapped to external memory |
| Window size | Number of visible 16-bit words |
| Backing address | Wider controller address used by the external memory device |
| Control block | Memory-mapped registers used to configure window/bank/latency |

If the external memory is larger than the visible OASIS window, the controller
may use bank registers, page registers, or DMA-style block transfer registers.
Portable code must not assume a banking scheme unless an extension profile or
platform header documents it.

## Minimal Memory-Mapped Control Block

An implementation that exposes configurable external memory should document a
control block with at least:

| Register | Purpose |
| -------- | ------- |
| `ID` | implementation/controller identifier |
| `CAPS` | capability bits such as read, write, burst, byte-lane support |
| `STATUS` | busy, ready, error, and initialization status |
| `CTRL` | enable, reset, clear-error, and optional interrupt-enable bits |
| `WINDOW_BASE` | OASIS word address where the external window begins |
| `WINDOW_SIZE` | visible window size in 16-bit words |
| `BANK` | selected backing bank/page, if banking is used |
| `WAIT` | timing or wait-state configuration |

The register addresses are platform-defined unless standardized by an extension.
Memory-mapped registers are 16-bit words.

## Ordering And Access Semantics

Base-16T has no cache model and no architectural memory fences. Therefore:

- Loads and stores issued by a simple in-order core should reach the controller
  in program order.
- A controller with wait states should stall the core or expose a ready/valid
  interface that preserves program order.
- A controller with asynchronous command registers should expose a `STATUS.busy`
  bit and require software polling before reading command results.
- If a future cache or DMA engine is added, its ordering rules must be defined
  by a new profile.

## ABI And Linker Expectations

Toolchains should not assume external memory exists. Platforms that provide it
should define linker symbols:

| Symbol | Purpose |
| ------ | ------- |
| `__oasis_extmem_start` | first external-memory word |
| `__oasis_extmem_end` | one past the final external-memory word |
| `__oasis_heap_start` | heap start, if heap lives in external memory |
| `__oasis_heap_end` | heap end |
| `__oasis_stack_top` | stack top, if stack lives in external memory |

C and C++ runtimes should use these symbols only when the platform linker script
provides them. The default Base-16T runtime remains internal-memory only.

## Optional Instruction Extension

The class `00` v0.2 exploration space reserves opcode `1101` as a candidate
external-memory or block-transfer template. No instruction is assigned yet.

Candidate future operations:

| Candidate | Purpose |
| --------- | ------- |
| `XMR` | read external-memory control register |
| `XMW` | write external-memory control register |
| `XMB` | select bank/page/window |
| `XMF` | memory fence or wait-until-ready |

These are placeholders. They should not be implemented as architectural OASIS
instructions until tables, assembler support, binutils support, and compliance
tests exist.

## Conformance Statement

An implementation with external memory should document:

- visible OASIS word-address range
- total backing memory size
- latency and stall behavior
- whether reads and writes are both supported
- whether external memory can hold stack, heap, globals, or program text
- memory-mapped control block address map
- reset values and initialization sequence
- any optional instruction extension profile
