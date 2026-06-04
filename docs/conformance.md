# OASIS Conformance

An implementation should claim the highest profile it fully implements and tests.

## Profiles

| Profile | Requirement |
| ------- | ----------- |
| Base-16 | Implements every non-toolchain instruction in OASIS v0.1 |
| Base-16T | Implements Base-16 plus every class `00` toolchain instruction |

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
5. Report profile coverage.

## Badges

Suggested badge text:

- `OASIS Base-16 v0.1 Draft: Tested`
- `OASIS Base-16T v0.1 Draft: Tested`

Do not claim a profile until every instruction in that profile is implemented
and covered by passing compliance tests.
