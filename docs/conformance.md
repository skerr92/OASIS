# OASIS Conformance

An implementation should claim the highest profile it fully implements and tests.

## Profiles

| Profile | Requirement |
| ------- | ----------- |
| Base-16 v0.1 | Implements every non-toolchain instruction in OASIS v0.1 |
| Base-16T v0.1 | Implements Base-16 plus every v0.1 class `00` toolchain instruction |
| Base-16 v0.2 | Implements Base-16 with `addr12` data-memory operands |
| Base-16T v0.2 | Implements Base-16 v0.2 plus the Base-16T ABI/toolchain instruction set |
| Base-16 v1.0 | Implements explicit `{mmio, addr11}` direct memory/MMIO operations |
| Base-16T v1.0 | Implements Base-16 v1.0 plus `{mmio, addr15}` indirect pointers, `MCP`, and the scratch ABI |

## Status Labels

Use these labels in implementation repositories:

- `Specified`: instruction is defined by OASIS
- `Implemented`: instruction exists in the core
- `Tested`: instruction passes OASIS compliance tests

## Compliance Tests

The shared tests live in `tests/compliance/`. Each YAML file declares a profile
and an assembly program with expected architectural state.

Implementation repositories should:

1. Import this repository as a pinned dependency.
2. Assemble each compliance program.
3. Run it on the implementation or simulator.
4. Compare expected register, memory, and program-counter state.
5. For tests with `expect.exit`, observe `CORE_PC`, select the exit-code
   register through `GPR_ADDR`, and compare `GPR_RDATA` with the expected code.
6. For tests with `expect.symbols`, verify the implementation's linked runtime
   or equivalent symbol map exposes the required runtime/linker symbols.
7. Complete [conformance-report-template.md](conformance-report-template.md) for
   release claims.
8. Report profile coverage.

## Badges

Suggested badge text:

- `OASIS Base-16 v0.1: Tested`
- `OASIS Base-16T v0.1: Tested`
- `OASIS Base-16 v0.2: Tested`
- `OASIS Base-16T v0.2: Tested`
- `OASIS Base-16 v1.0: Tested`
- `OASIS Base-16T v1.0: Tested`

Do not claim a profile until every instruction in that profile is implemented
and covered by passing compliance tests.
