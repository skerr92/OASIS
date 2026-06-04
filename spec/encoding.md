# Encoding

OASIS v0.1 instructions are 32 bits wide. Multi-bit fields are encoded
most-significant bit first.

## Common Fields

| Bits | Field | Meaning |
| ---- | ----- | ------- |
| `[31:30]` | `class` | Instruction class |
| `[29:26]` | `opcode4` | ALU/jump opcode for class `01` |
| `[29:28]` | `opcode2` | Register or memory opcode for classes `10` and `11` |

## Classes

| Class | Name | Meaning |
| ----- | ---- | ------- |
| `00` | Toolchain | Base-16T toolchain operations; reserved in Base-16 |
| `01` | ALU | ALU and jump operations |
| `10` | Register | Register move and immediate operations |
| `11` | Memory | Data memory operations |

Reserved fields must be encoded as zero. Portable software must not rely on any
behavior for invalid encodings.

## Base-16T

Base-16T defines class `00` for toolchain-oriented instructions needed by C and
C++ compiler targets: immediate arithmetic, register-indirect memory access,
call/return, register jump, and signed/unsigned comparison branches.

See [../tables/encoding-fields.csv](../tables/encoding-fields.csv) for the
machine-readable field table.
