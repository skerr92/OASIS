# OASIS-16 v1.0.0-rc.1 Release Notes

This release candidate establishes the first hard compatibility boundary after
the OASIS v0.x experimental series.

## Architectural Changes

- Direct `MVF`, `MVT`, and `MSI` operands explicitly select ordinary memory or
  MMIO and use an 11-bit address within the selected space.
- Base-16T pointers retain a full 15-bit address plus the space selector.
- `MCP` and the `sap`/`sdata` scratch ABI support staged transfers to far memory
  and MMIO destinations. `MSI`/`MCP` remains intentionally interruptible.
- OASIS-16P optionally adds User/Machine modes, precise traps, 16 interrupt
  sources, system registers, `TRAP`, `ERET`, `WFI`, and CSR operations.

## Toolchain and Compliance

- GCC 14.3.0 and binutils 2.46 backends implement the v1.0 memory contract.
- Native GAS and objdump implement all seven OASIS-16P grouped suboperations.
- Exact-byte fixtures cover valid and malformed P-profile encodings.
- An executable system-block model covers trap entry/return, CSR behavior,
  interrupt arbitration, wait/wake behavior, privilege faults, and MMIO faults.

## Compatibility

v0.x binaries are not encoding-compatible with v1.0 memory operations and must
be rebuilt. Implementations without OASIS-16P remain conforming Base-16 or
Base-16T implementations when they report the extension as unsupported.

OASIS-32 and DungV-32 remain planned profiles, not release-candidate RTL.
