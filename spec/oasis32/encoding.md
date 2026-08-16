# OASIS-32 Encoding

Status: experimental planning draft.

OASIS-32 uses fixed-width 64-bit instructions. Fixed width keeps decode simple
and gives the ISA enough room for regular register fields and 32-bit immediates.

## Universal Header

Every OASIS-32 instruction starts with the same field layout:

```text
63        60 59        56 55        48 47        40 39        32 31                  0
+------------+------------+------------+------------+------------+----------------------+
| class[3:0] | op[3:0]    | rd[7:0]    | ra[7:0]    | rb[7:0]    | imm/func/extra[31:0] |
+------------+------------+------------+------------+------------+----------------------+
```

Field meanings should remain as stable as possible across instruction formats:

| Field | Bits | Meaning |
| ----- | ---- | ------- |
| `class` | `63:60` | Top-level instruction class |
| `op` | `59:56` | Primary operation within the class |
| `rd` | `55:48` | Destination register or source register for stores |
| `ra` | `47:40` | First source or base register |
| `rb` | `39:32` | Second source, address-space/size mode, condition, or flags |
| `imm32` | `31:0` | Immediate, offset, function bits, or extension payload |

## Canonical Formats

OASIS-32 should avoid one-off encodings. The initial canonical formats are:

| Format | Purpose |
| ------ | ------- |
| `R` | register-register operations |
| `I` | register-immediate operations |
| `M` | load/store with base plus signed offset |
| `B` | conditional branches with signed PC-relative offset |
| `J` | jumps, calls, returns, and indirect control flow |
| `U` | constants and upper/lower immediate construction |
| `S` | system, trap, and special operations |

Detailed draft layouts are recorded in `tables/oasis32/encoding-formats.csv`.

## Immediate Policy

`imm32` is interpreted by instruction class and format. Signed arithmetic,
memory offsets, branches, and calls should sign-extend `imm32`. Logical
immediates may use zero-extension or full 32-bit literal interpretation as
defined by each instruction.

`MVI rd, imm32` should directly materialize any 32-bit constant in Base-32T.

## Memory Space Bit

M-format instructions reserve a `space` bit in `space_size_flags`: `0` selects
ordinary memory and `1` selects MMIO. This selector is independent of the full
32-bit base and signed-offset calculation. The exact subfield position will be
frozen with the Base-32 opcode table; implementations must not infer the space
from the numeric address.
