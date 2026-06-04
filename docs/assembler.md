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
- Registers are `r0` through `r63`
- Immediates may be decimal, `0b` binary, or `0x` hexadecimal
- Absolute memory operands use brackets, such as `[0x001]`
- Base-16T register-relative memory operands use `[rN]`, `[rN + off6]`, or `[rN - off6]`

Example:

```asm
start:
MVI r1, 10
MVI r2, 20
ADD r1, r2
MVT r1, [0x001]
JMP start
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

See [programming-cores.md](programming-cores.md) for programming flows.
