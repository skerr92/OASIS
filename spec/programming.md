# Programming Model

OASIS Base-16 cores need a way to load 32-bit instruction words into program
memory. The ISA does not require a specific electrical interface, but compliant
tooling should be able to produce images that SPI, JTAG, or simulation loaders
can consume.

## Instruction Memory

Base-16 instruction memory is addressed by 8-bit instruction index and stores
one 32-bit instruction per address.

| Field | Value |
| ----- | ----- |
| Address width | 8 bits |
| Instruction width | 32 bits |
| Instruction count | 256 |
| Reset fetch address | `0x00` |

Programming is not architecturally visible to running software. A core should be
halted or held in reset while program memory is modified.

## Recommended Programming Access Port

The recommended debug/programming access port is transport-neutral. SPI and JTAG
bridges can both expose this same 16-bit register map.

| Address | Name | Access | Description |
| ------- | ---- | ------ | ----------- |
| `0x0000` | `CONTROL` | RW | Control bits |
| `0x0001` | `STATUS` | RO | Status bits |
| `0x0002` | `CORE_ID` | RO | Implementation-defined core identifier |
| `0x0003` | `OASIS_PROFILE` | RO | OASIS profile identifier |
| `0x0004` | `IMEM_ADDR` | RW | 8-bit instruction memory address |
| `0x0005` | `IMEM_WDATA_LO` | RW | Instruction write data bits `[15:0]` |
| `0x0006` | `IMEM_WDATA_HI` | RW | Instruction write data bits `[31:16]` |
| `0x0007` | `IMEM_RDATA_LO` | RO | Instruction read data bits `[15:0]` |
| `0x0008` | `IMEM_RDATA_HI` | RO | Instruction read data bits `[31:16]` |

`CONTROL` bits:

| Bit | Name | Description |
| --- | ---- | ----------- |
| `0` | `HALT` | Hold the core halted when set |
| `1` | `RESET` | Hold the core in reset when set |
| `2` | `IMEM_WRITE` | Write `IMEM_WDATA_HI:IMEM_WDATA_LO` to `IMEM_ADDR` when strobed |
| `3` | `IMEM_READ` | Read `IMEM_ADDR` into `IMEM_RDATA_HI:IMEM_RDATA_LO` when strobed |
| `4` | `AUTO_INC` | Increment `IMEM_ADDR` after instruction memory access |

`STATUS` bits:

| Bit | Name | Description |
| --- | ---- | ----------- |
| `0` | `HALTED` | Core is halted |
| `1` | `RESETTING` | Core reset is asserted |
| `2` | `BUSY` | Programming access is in progress |
| `3` | `ERROR` | Last programming access failed |

## Programming Sequence

Recommended sequence:

1. Assert `HALT` and `RESET`.
2. Set `IMEM_ADDR` to the first instruction index.
3. For each instruction, write low 16 bits to `IMEM_WDATA_LO`.
4. Write high 16 bits to `IMEM_WDATA_HI`.
5. Strobe `IMEM_WRITE`; use `AUTO_INC` for streaming writes.
6. Optionally read back instruction memory through `IMEM_READ`.
7. Release `RESET`.
8. Release `HALT` when the program should start.

## SPI Transport

SPI is a good fit for small 16-bit designs. Recommended framing:

| Byte | Field |
| ---- | ----- |
| `0` | Command |
| `1` | Register address high byte |
| `2` | Register address low byte |
| `3` | Data high byte for writes |
| `4` | Data low byte for writes |

Commands:

| Command | Meaning |
| ------- | ------- |
| `0x01` | 16-bit register write |
| `0x02` | 16-bit register read |

The SPI bridge translates register reads/writes into the programming access port
above.

## JTAG Transport

JTAG is usually the least painful option for FPGA and debug-heavy workflows. A
JTAG bridge should expose the same 16-bit programming access port through either
a simple debug register chain or a vendor debug bridge.

JTAG is recommended when:

- The FPGA board already has a JTAG connector
- Readback and debug are important
- The core shares programming infrastructure with other debug features

SPI is recommended when:

- Pin count is constrained
- A microcontroller or flash chip will program the core
- The board does not expose JTAG conveniently
