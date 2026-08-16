# DungV v1 and DungV-32 Integration

This document tracks downstream implementation of the OASIS v1.0 memory/MMIO
contract and the optional OASIS-16P/OASIS-32P system block. DungV pins
OASIS v1.0.0-rc.1 commit `251f2a3` and records implementation evidence in its
own compatibility report.

## DungV v1 Upgrade

1. **Complete:** advance the OASIS submodule to `251f2a3` and record the target
   in DungV's compatibility report.
2. **Base-16 direct path complete and hardware verified:** decode direct memory
   operands as `{mmio, addr11}` and route ordinary memory and MMIO to distinct
   request paths. `{mmio, addr15}` indirect pointers remain Base-16T work.
3. **Open:** implement `MCP`, the `sap`/`sdata` ABI roles, and the configurable ordinary-
   memory scratch range. Preserve the specified interruptible two-instruction
   `MSI`/`MCP` behavior.
4. **Base-16 handshake complete and hardware verified:** add request,
   completion, and error handshakes to the memory/MMIO boundary. Precise cause
   conversion remains open until OASIS-16P is present.
5. **Open:** add the reusable system block described in `spec/exceptions.md`. The core
   supplies retirement boundaries and precise PCs; the block owns arbitration,
   system registers, privilege checks, trap capture, `WFI`, and redirect.
6. **In progress:** run base v1.0 compliance first, then report OASIS-16P separately as an
   optional profile. Base behavior must remain valid when the system block is
   disabled.

## Verified DungV MMIO Milestone

DungV commit
[`3425421`](https://github.com/skerr92/DungV/commit/3425421a3b113d3e13b53f84e32a649007d5a94c)
provides the implementation evidence for the direct Base-16 boundary:

- ordinary memory and MMIO use separate, non-aliasing 2048-word spaces;
- `MVF`, `MVT`, and `MSI` drive a held request until completion;
- GPIO and atomic RGB PWM writes were observed on RPGA hardware;
- blocking UART MMIO passed repeated 115200-baud echo exchanges;
- open-drain I2C addressed a BMA530 at `0x18` and returned CHIP_ID `0xC2`;
- peripheral RTL tests cover GPIO access/error behavior, exact PWM duty counts,
  UART loopback, and I2C START/write/ACK/read/STOP behavior.

This closes the v1.0 direct-MMIO hardware milestone. It does not close the
Base-16T scratch/indirect work or optional OASIS-16P precise-fault work.

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
