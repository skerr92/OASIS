# Programming OASIS Cores

OASIS implementation repositories can consume this repo as a submodule and use
the assembler plus programming-image tools to load program memory.

## Core Requirements

A programmable Base-16 core should provide:

- A writable instruction memory path
- A way to halt or reset the core during programming
- Optional instruction-memory readback
- A transport bridge, commonly SPI or JTAG

The recommended transport-neutral register map is defined in
[spec/programming.md](../spec/programming.md).

## Instruction Memory RTL Guidance

Avoid making instruction memory load-only through `$readmemb` or FPGA
initialization files. Prefer a memory module with two access paths:

- Core fetch port: `pc -> instruction`
- Programming port: `prog_addr`, `prog_wdata`, `prog_we`, `prog_rdata`

During programming, the core should be halted or reset so fetch does not race
against writes. Implementations may use a dual-port RAM, a muxed single-port RAM,
or a small bus fabric.

## SPI Flow

1. Assemble source with `bin/oasis-asm`.
2. Convert the program into a programming script with `bin/oasis-program-image`.
3. Send register writes over an SPI bridge.
4. Release reset/halt.

SPI is compact and easy to drive from a microcontroller.

## JTAG Flow

1. Assemble source with `bin/oasis-asm`.
2. Convert the program into the same programming script.
3. Feed register writes through a JTAG bridge.
4. Optionally read back instruction memory for verification.
5. Release reset/halt.

JTAG is preferred for FPGA development because it naturally supports debug,
readback, and board bring-up.
