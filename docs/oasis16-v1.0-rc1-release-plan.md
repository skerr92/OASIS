# OASIS-16 v1.0.0-rc.1 Release Plan

Status: candidate preparation complete; awaiting review, commit, and tag.

The first v1.0 release candidate freezes the explicit memory/MMIO boundary and
provides the architectural and toolchain contract needed to begin DungV FPGA
integration on the RPGA Feather.

## Candidate Scope

- Base-16 and Base-16T v1.0 `{mmio, addr11}` direct-memory encodings.
- Full `{mmio, addr15}` indirect pointers, the scratch ABI, and `MCP`.
- GCC 14.3.0 and binutils 2.46 native backend integration.
- Optional OASIS-16P interrupt, trap, and privilege architecture.
- Native GAS/objdump support for all OASIS-16P system instructions.
- Executable reference-model coverage for OASIS-16P architectural state.
- OASIS-32P roadmap mapping and DungV/DungV-32 integration requirements.

## Release Gate

- [x] `make generate` completes without uncommitted generated drift.
- [x] `make check` passes.
- [x] `git diff --check` passes.
- [x] Native Darwin arm64 GCC/binutils rebuild passes installed validation.
- [x] P-profile exact encoding and disassembly fixtures pass native tools.
- [x] P-profile trap, CSR, interrupt, `WFI`, and `ERET` model tests pass.
- [ ] Review the candidate diff and commit it on `v1.0_source`.
- [ ] Build and checksum source and Darwin arm64 toolchain archives.
- [ ] Push tag `v1.0.0-rc.1` and attach release artifacts.

## DungV Entry Condition

Once the candidate commit and tag exist, DungV may pin that exact commit and
start the sequence in [dungv-v1-integration.md](dungv-v1-integration.md). The
first hardware milestone is base v1.0 decode plus separate ordinary-memory and
MMIO handshakes on the RPGA Feather. OASIS-16P integration follows behind the
same retirement/redirect boundary exercised by the executable model.

The release candidate does not claim an FPGA implementation. DungV simulation,
board timing, peripheral electrical behavior, and RPGA Feather programming are
downstream qualification gates.
