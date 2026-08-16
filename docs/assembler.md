# OASIS Base-16 Assembler

`tools/oasis_asm.py` assembles OASIS Base-16 assembly into 32-bit instruction
words. `bin/oasis-asm` is a convenience wrapper for consumers that add this
repository as a submodule.

## Usage

```sh
bin/oasis-asm examples/base16/add_store.oas -o add_store.mem
```

Output formats:

| Format | Description |
| ------ | ----------- |
| `binstr` | Default. One 32-bit binary instruction per line for Verilog `$readmemb`. |
| `hex` | One 8-digit hexadecimal instruction per line. |
| `raw-be` | Raw 32-bit words in big-endian byte order. |
| `raw-le` | Raw 32-bit words in little-endian byte order. |

## Supported Syntax

- One instruction per line
- Comments start with `;`
- Labels end with `:`
- Registers are `r0` through `r63`; `sap` aliases `r59` and `sdata` aliases `r60`
- Immediates may be decimal, `0b` binary, or `0x` hexadecimal
- Direct operands require an explicit space: `mem:[addr11]` or `io:[addr11]`
- Far pointer immediates use `mem:addr15` or `io:addr15`
- Base-16T register-relative memory operands use `[rN]`, `[rN + off6]`, or `[rN - off6]`

Example:

```asm
start:
MVI r1, 10
MVI r2, 20
ADD r1, r2
MVT r1, mem:[0x001]
JMP start
```

The assembler rejects unqualified direct operands and addresses above
`0x07ff`. A staged far write uses:

```asm
MVI sap, io:0x0100
MSI mem:[0x0000], 0x1234
MCP [sap], mem:[0x0000]
```

## Submodule Consumption

Implementation repositories can call the assembler from a submodule path:

```sh
external/OASIS/bin/oasis-asm program.oas -o program.mem
```

The assembler has no third-party Python dependencies.

## Programming Images

`bin/oasis-program-image` converts assembly into programming artifacts for the
recommended OASIS programming access port.

```sh
bin/oasis-program-image examples/base16/add_store.oas -o add_store.dap16
bin/oasis-program-image examples/base16/add_store.oas --format spi16-hex -o add_store.spi16
```

Formats:

| Format | Description |
| ------ | ----------- |
| `dap16` | Transport-neutral 16-bit register write script. |
| `spi16-hex` | SPI write frames encoded as hexadecimal text. |

## ELF Images

`bin/oasis-elf2img` converts linked or relocatable `elf32-oasis16` files into the
same programming image formats. It extracts the first executable `PT_LOAD`
segment when present, otherwise it falls back to `.text`.

```sh
bin/oasis-elf2img hello.elf -o hello.dap16
bin/oasis-elf2img hello.elf --format spi16-hex -o hello.spi16
```

Diagnostic formats are also available:

| Format | Description |
| ------ | ----------- |
| `hex` | One 8-digit hexadecimal instruction per line. |
| `binstr` | One 32-bit binary instruction per line. |

See [programming-cores.md](programming-cores.md) for programming flows.
