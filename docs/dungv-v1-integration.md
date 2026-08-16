# DungV v1 and DungV-32 Integration

This document is the downstream implementation sequence for the OASIS v1.0
memory/MMIO contract and the optional OASIS-16P/OASIS-32P system block. Work in
the DungV repository begins after v1.0 is merged to the OASIS default branch so
its submodule can advance to a stable architectural commit.

## DungV v1 Upgrade

1. Advance the OASIS submodule and record the exact v1.0 commit in the DungV
   conformance report.
2. Decode direct memory operands as `{mmio, addr11}` and indirect pointers as
   `{mmio, addr15}`. Route ordinary memory and MMIO to distinct request paths.
3. Implement `MCP`, the `sap`/`sdata` ABI roles, and the configurable ordinary-
   memory scratch range. Preserve the specified interruptible two-instruction
   `MSI`/`MCP` behavior.
4. Add request, completion, and error handshakes to the memory/MMIO boundary.
   Convert failed fetch, load, store, and MMIO transactions into the standard
   precise causes when OASIS-16P is present.
5. Add the reusable system block described in `spec/exceptions.md`. The core
   supplies retirement boundaries and precise PCs; the block owns arbitration,
   system registers, privilege checks, trap capture, `WFI`, and redirect.
6. Run base v1.0 compliance first, then report OASIS-16P separately as an
   optional profile. Base behavior must remain valid when the system block is
   disabled.

## DungV-32 Bring-up

DungV-32 should reuse the verified system block through a width-parameterized
interface rather than fork its trap state machine. Its initial milestone is an
OASIS-32I pipeline with the explicit memory/MMIO space bit. The next milestone
adds OASIS-32P class `0xE` operations and class `0x0` `TRAP`, followed by an
executable compliance model and interrupt/MMIO fault tests.

The two implementations share architectural register IDs, cause IDs, priority,
entry ordering, and return behavior. They do not share instruction decode or PC
width assumptions. DungV-32 also retains full 32-bit addresses and does not
require the OASIS-16 scratch convention.

## Required Integration Tests

- ordinary memory and MMIO never alias for identical low address bits;
- failed operations report the correct access-fault class and `TVAL` address;
- a `TRAP imm8` records the following PC and zero-extends `imm8` into `TVAL`;
- interrupt priority is lowest source ID first and respects both masks;
- interrupt entry between `MSI` and `MCP` preserves the architectural contract;
- `ERET` restores mode, PC, and interrupt enable exactly once;
- disabled OASIS-16P decode reports optional system instructions as unsupported.
