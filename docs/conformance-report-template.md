# OASIS-16 Conformance Report Template

Use this template when an implementation claims compatibility with an OASIS-16
profile. Keep the completed report with the implementation repository and link
it from release notes or hardware documentation.

## Implementation

| Field | Value |
| ----- | ----- |
| Implementation name | |
| Repository or source package | |
| Hardware target or simulator | |
| OASIS version | v1.0 |
| Profile | Base-16 / Base-16T |
| Report date | |
| Commit, tag, or artifact ID | |

## Architectural Coverage

| Requirement | Supported | Evidence |
| ----------- | --------- | -------- |
| 16-bit data path | | |
| 32-bit instruction words | | |
| 64 writable general purpose registers | | |
| Word-addressed data memory | | |
| Explicit `{mmio, addr11}` direct operands | | |
| `{mmio, addr15}` Base-16T indirect pointers | | |
| `MCP` scratch-to-far transfer, if Base-16T | | |
| Base-16 instruction set | | |
| Base-16T instruction set, if claimed | | |
| Reset behavior | | |
| Invalid or reserved encoding behavior documented | | |

## Memory Map

| Region | Base | Limit | Notes |
| ------ | ---- | ----- | ----- |
| Instruction memory | | | |
| Data memory | | | |
| Scratch reservation | | | |
| Stack | | | |
| Heap, if provided | | | |
| Memory-mapped IO | | | |
| External memory window, if provided | | | |

## Toolchain And Runtime

| Requirement | Supported | Evidence |
| ----------- | --------- | -------- |
| OASIS assembler accepts required programs | | |
| Programming image generation works | | |
| GCC/binutils build or installed-toolchain smoke tests pass | | |
| Base-16T ABI register roles followed, if claimed | | |
| Scratch linker symbols and exclusion verified | | |
| Stack frame and call/return behavior verified | | |
| Runtime exit/debug observation convention documented | | |
| C++ init-array and guard hooks available, if claimed | | |

## Compliance Tests

Record the exact command lines and results used for the claim.

```text
make check
```

```text
<implementation-specific compliance command>
```

| Test suite | Result | Notes |
| ---------- | ------ | ----- |
| OASIS opcode/table validators | | |
| OASIS assembler tests | | |
| OASIS compliance YAML programs | | |
| Implementation simulation tests | | |
| Hardware smoke tests | | |
| Toolchain compile/link smoke tests | | |

## Deviations

List every unsupported feature, implementation-defined behavior, timing
assumption, or extension required to reproduce the report.

| Item | Description | Impact |
| ---- | ----------- | ------ |
| | | |

## Optional Extensions

| Extension | Status | Evidence |
| --------- | ------ | -------- |
| External memory control | | |
| Peripheral instructions | | |
| Debug/halt interface | | |
| OASIS-16P interrupts, traps, and privilege | | |

## Claim

```text
<implementation name> claims conformance with OASIS-16 <version> <profile>
for the commit/artifact listed above, subject to the deviations listed in this
report.
```
