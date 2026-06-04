# OASIS Base-16T

Base-16T is the OASIS v0.1 toolchain profile. It extends Base-16 with the
minimum ISA mechanisms needed for freestanding C and C++ compiler targets.

## Relationship To Base-16

Base-16T includes every Base-16 instruction and defines class `00`, which is
reserved by Base-16.

| Profile | Class `00` behavior |
| ------- | ------------------- |
| Base-16 | Reserved |
| Base-16T | Toolchain operations |

## Added Capabilities

| Capability | Instructions |
| ---------- | ------------ |
| Immediate arithmetic | `ADI`, `SBI` |
| Stack/register-relative memory | `LDR`, `STR` |
| Function calls | `CALL`, `RET` |
| Indirect control flow | `JMR` |
| Signed comparisons | `JLT`, `JGE` |
| Unsigned comparisons | `JLTU`, `JGEU` |

## Encoding Formats

Immediate arithmetic:

| Bits | Field |
| ---- | ----- |
| `[31:30]` | `00` class |
| `[29:26]` | opcode |
| `[25:20]` | `ra` |
| `[19:16]` | reserved |
| `[15:0]` | `imm16` |

Register-indirect memory:

| Bits | Field |
| ---- | ----- |
| `[31:30]` | `00` class |
| `[29:26]` | opcode |
| `[25:20]` | data register `ra` |
| `[19:14]` | base register `rb` |
| `[13:8]` | signed word offset `off6` |
| `[7:0]` | reserved |

Toolchain branch:

| Bits | Field |
| ---- | ----- |
| `[31:30]` | `00` class |
| `[29:26]` | opcode |
| `[25:20]` | left register `ra` |
| `[19:14]` | right register `rb` |
| `[13:6]` | absolute target `target8` |
| `[5:0]` | reserved |

Call and return use the same class/opcode region. `CALL` uses `target8` in bits
`[13:6]`; `RET` has no operands. `JMR` uses `rb` in bits `[19:14]`.

## C And C++ Support

Base-16T is the intended target for:

- `oasis16-unknown-elf`
- `oasis16-elf-gcc`
- `oasis16-elf-g++`
- `oasis16-elf-as`
- `oasis16-elf-ld`

The ABI draft lives in
[../toolchain/abi/base16-baremetal-abi.md](../toolchain/abi/base16-baremetal-abi.md).

## Implementation Requirement

A core claiming Base-16T support must implement all Base-16 instructions and all
Base-16T class `00` instructions.
