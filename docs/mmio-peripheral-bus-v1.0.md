# OASIS v1.0 MMIO and Peripheral Bus Design

Status: accepted v1.0 architecture rationale; normative encodings live in the
specification and machine-readable tables.

## Goal

OASIS v1.0 introduces an architecture-defined peripheral address space. Direct
memory instructions select ordinary data memory or memory-mapped I/O (MMIO)
explicitly, rather than consuming vendor-defined instruction encodings for
basic peripheral access.

The selector is part of the address operand and is encoded immediately before
the address field:

```text
address operand = { mmio, address }
```

`mmio = 0` selects ordinary data memory. `mmio = 1` selects the peripheral
space. The two spaces may use the same numeric address without aliasing.

## v1.0 Requirements

1. `MVF`, `MVT`, and `MSI` encode an explicit `mmio` selector before every
   direct address.
2. Ordinary memory and MMIO are distinct architectural spaces.
3. Every direct memory operation uses the same 12-bit `{mmio, addr11}` operand.
4. Peripheral access does not require a vendor opcode.
5. Vendor instruction areas remain available for acceleration and operations
   that cannot be represented as ordinary register reads and writes.
6. `MSI` continues to make all 16 immediate bits available and remains one
   32-bit instruction word.
7. Addresses outside the direct 11-bit per-space window use an explicitly
   documented register-indirect sequence.
8. The Base-16T ABI defines a configurable ordinary-memory scratch block, with
   `0x0000` through `0x001F` as the default reservation.
9. OASIS-32 is evaluated separately; Base-16 encoding constraints are not
   imposed on it merely for encoding symmetry.

## Existing Encoding Budget

All Base-16 instructions occupy one 32-bit instruction word.

| Instruction | Fixed fields | Current operands | Spare bits |
| --- | --- | --- | --- |
| `MVF`/`MVT` | class 2 + opcode 2 | register 6 + address 12 | 10 |
| `MSI` | class 2 + opcode 2 | address 12 + immediate 16 | 0 |

Although `MVF` and `MVT` have spare bits, v1.0 intentionally retains a uniform
direct-address operand. In all three instructions, the high bit of the former
12-bit address field becomes `mmio` and the remaining 11 bits select a word in
that space.

## Uniform Direct-Address Layout

`MVF` and `MVT` use this layout:

| Bits | Field | Meaning |
| --- | --- | --- |
| `31:30` | `class` | `11`, memory class |
| `29:28` | `opcode` | `01` for `MVF`, `10` for `MVT` |
| `27:22` | `ra` | transferred register |
| `21` | `mmio` | 0 data memory, 1 peripheral space |
| `20:10` | `addr11` | word address within the selected space |
| `9:0` | `reserved` | must be zero |

`MSI` uses the same logical operand in bits 27:16:

| Bits | Field | Meaning |
| --- | --- | --- |
| `31:30` | `class` | `11`, memory class |
| `29:28` | `opcode` | `11`, MSI |
| `27` | `mmio` | 0 data memory, 1 peripheral space |
| `26:16` | `addr11` | 11-bit word address within the selected space |
| `15:0` | `imm16` | immediate value to store |

The three direct operations are therefore:

```text
MVF: ra = space[mmio][addr11]
MVT: space[mmio][addr11] = ra
MSI: space[mmio][addr11] = imm16
```

This provides 2048 directly selectable words in ordinary data memory and 2048
directly selectable words in MMIO. Across the two non-aliasing spaces, every
12-bit `{mmio, addr11}` value still identifies a unique architectural location.
The original 12-bit selection capacity is therefore retained, while its most
significant bit now has explicit address-space semantics.

Each instruction performs one architecturally visible access to its selected
destination. Internal implementation staging is not observable.

### Consequences

- MSI remains fixed-width and keeps its full 16-bit immediate.
- Base-16 does not need variable-length instruction fetch for MSI.
- The MSI instruction itself does not require architected scratch storage; the
  Base-16T ABI reservation below supports explicit staged-transfer sequences.
- All direct memory instructions reach the low 2048 words of either space.
- The ten low reserved bits in `MVF` and `MVT` remain available for future use.
- Addresses beyond `0x07FF` require register-indirect access.

## Far Addresses and Scratch Convention

### Full pointer representation

A Base-16T data pointer is 16 bits:

```text
bit 15    = mmio
bits 14:0 = word address within the selected space
```

For `LDR` and `STR`, the effective signed offset applies only to bits 14:0 and
must not change the space bit. Address overflow or underflow within a space
wraps modulo 32768. This gives register-indirect operations a 32768-word reach
in each space while keeping the direct instructions compact and uniform.

### ABI registers

Base-16T v1.0 assigns two previously reserved registers:

| Register | Alias | Role | Volatility |
| --- | --- | --- | --- |
| `r59` | `sap` | scratch/far-address pointer | caller-saved |
| `r60` | `sdata` | scratch transfer value | caller-saved |

Base-16 hardware still treats both as ordinary writable registers. Assembly
that does not use the Base-16T ABI may choose any registers. Reserving only
`r59` is insufficient with the existing ISA because `LDR` and `STR` transfer
through a register; a memory-to-memory move does not currently exist.

### Scratch block

The default Base-16T platform memory map reserves ordinary data-memory words
`0x0000` through `0x001F` as a 32-word scratch block. The clean power-of-two
boundary simplifies decoding and allocation. A platform may choose a different
size or location, including no scratch block, but must publish:

- `__oasis_scratch_start`, the first reserved word;
- `__oasis_scratch_end`, one word past the reservation;
- `__oasis_scratch_words`, the reservation size.

The linker must exclude this range from `.data`, `.bss`, heap, and stack. MMIO
addresses `0x0000` through `0x001F` are unrelated and are not reserved by this
ABI convention.

Scratch allocation is a software concern. Interrupt handlers, concurrent tasks,
DMA, and multiple cores must not share a live slot without synchronization.
Implementations may partition the block by execution context or override the
default reservation.

### Required expansions

An immediate store to a far address does not require scratch memory:

```asm
MVI sap, encoded_far_pointer
MVI sdata, imm16
STR sdata, [sap + 0]
```

If software explicitly requires the immediate to pass through valid scratch
memory, the expansion is:

```asm
MVI sap, encoded_far_pointer
MSI mem:[scratch_slot], imm16
MVF sdata, mem:[scratch_slot]
STR sdata, [sap + 0]
```

The latter performs two architecturally visible writes: first to ordinary
scratch memory, then to the final memory or MMIO destination. With the existing
ISA, it needs three memory instructions after the pointer is prepared. The
assembler and compiler must not collapse it into an atomic operation, and a
fault or interrupt may occur between the two writes.

The compiler should use the shorter register-only expansion unless a platform
contract specifically requires observable scratch staging. A future
memory-to-memory instruction could shorten the staged form, but v1.0 should not
give an existing opcode hidden stateful semantics merely to make it appear
two-operation.

### Two-operation transfer

The v1.0 baseline adds a memory-copy-word instruction rather than changing MSI
implicitly. Syntax:

```asm
MCP [sap], mem:[scratch_slot]
```

Operation:

```text
space[sap.mmio][sap.addr15] = memory[scratch_slot]
```

The source is always ordinary data memory and must lie inside the platform's
published scratch block. The destination comes from an explicit pointer
register, whose high bit selects memory or MMIO. The 32-bit encoding uses
Base-16T toolchain opcode `00:1100`:

| Bits | Field | Meaning |
| --- | --- | --- |
| `31:30` | `class` | `00`, Base-16T toolchain class |
| `29:26` | `opcode` | `1100`, MCP |
| `25:20` | `rb` | destination pointer register |
| `19:9` | `scratch11` | ordinary-memory scratch source |
| `8:0` | `reserved` | must be zero |

After `sap` has been prepared, a staged immediate-to-far write becomes exactly
two explicit memory operations:

```asm
MSI mem:[scratch_slot], imm16
MCP [sap], mem:[scratch_slot]
```

`MCP` is not atomic with the preceding `MSI`. It performs one source read and
one destination write; MMIO side effects occur only at its destination. The
source must remain unchanged between the instructions, so interrupt and
concurrency rules still apply. A fallback assembler may expand the transfer
into the existing `MVF sdata` plus `STR sdata` pair when targeting pre-v1.0
hardware, but that output is not v1.0-equivalent binary code.

### Assembly explicitness

Source syntax identifies the address space rather than inferring it from a
numeric address:

```asm
MVF r1, mem:[0x0040]
MVT r1, io:[0x0040]
MSI mem:[0x0000], 0x1234
```

The assembler must reject a direct address above `0x07FF` and direct the author
to a register-indirect or far-address pseudo-operation. Compiler diagnostics,
disassembly, relocations, and linker maps must preserve the memory/MMIO space
explicitly.

## Peripheral Bus Contract to Specify

The ISA should define the CPU-facing transaction independently of a particular
on-chip bus protocol. At minimum, an MMIO access needs:

- word address;
- 16-bit write data or 16-bit read data;
- read/write direction;
- request and completion handshake;
- fault/error result;
- ordering rules relative to earlier and later memory and MMIO accesses;
- behavior for unsupported addresses and access timeouts.

Implementations may bridge this contract to Wishbone, APB, AXI-Lite, a custom
fabric, or discrete peripheral selects. These bridges are implementation
details and do not change architectural instruction semantics.

## Baseline Decisions

- `mem:[addr11]` and `io:[addr11]` are the normative direct assembly forms.
- Base-16T indirect pointers use `{mmio, addr15}` and offsets wrap within the
  selected space.
- Ordinary memory `0x0000` through `0x001f` is the default scratch reservation;
  platform linker scripts may override it and must publish the scratch symbols.
- `MCP` is Base-16T opcode `00:1100`.
- MMIO accesses issue in program order. Reads may have platform-documented side
  effects; unsupported accesses report the implementation's defined bus fault
  or error behavior.
