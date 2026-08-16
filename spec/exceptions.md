# Interrupts, Traps, and Privilege

OASIS v1.0 defines the optional `OASIS-16P` interrupt, trap, and privilege
extension. OASIS-32 carries the same state-transition contract as `OASIS-32P`
with wider registers and independent instruction encodings.

Base-16 and Base-16T implementations without `OASIS-16P` remain valid. They
must report unsupported system instructions as invalid according to their
conformance statement. A core advertising `OASIS-16P` must implement this
entire document.

## Privilege Modes

| Mode | Encoding | Purpose |
| --- | --- | --- |
| User (`U`) | `0` | Applications and unprivileged runtime code |
| Machine (`M`) | `1` | Firmware, handlers, and platform control |

Reset enters Machine mode with interrupts disabled. Machine mode may execute
all instructions and access every system register. User mode may execute
`TRAP`; other privileged instructions and protected system-register accesses
raise a privilege-violation exception.

This initial two-mode contract omits virtual memory, supervisor mode, hypervisor
mode, and delegation. Those features require later profiles.

## Architectural System Registers

System registers have the architectural register width: 16 bits in OASIS-16P
and 32 bits in OASIS-32P. Register IDs and access rules are defined in
[`tables/system-registers.csv`](../tables/system-registers.csv).

`STATUS` uses these low bits in both profiles:

| Bit | Name | Meaning |
| --- | --- | --- |
| `0` | `IE` | Global maskable-interrupt enable |
| `1` | `PIE` | Saved pre-trap `IE` |
| `2` | `MODE` | Current mode: 0 User, 1 Machine |
| `3` | `PMODE` | Saved pre-trap mode |
| `4` | `WFI` | Read-only indication that the core is waiting |

Unspecified `STATUS` bits read as zero and ignore writes. `TVEC` and `EPC` use
instruction addresses. OASIS-16P uses their low 8 bits; OASIS-32P uses the
implemented instruction-address width.

`SYSINFO` bit 0 (`PRESENT`) is one when this block is implemented. Bits 15:8
contain the block ABI major version, initially zero; all other bits are reserved
and read as zero. This makes reset value `0x0001` valid for the first version.

`CAUSE` contains an interrupt flag in its most significant bit. For synchronous
traps that bit is zero and the remaining bits contain a cause code. For
interrupts it is one and the low bits contain the interrupt source ID. Standard
codes are defined in [`tables/trap-causes.csv`](../tables/trap-causes.csv).

`TVAL` contains cause-specific information when available:

- illegal instruction: low architectural word of the instruction;
- access fault: faulting address, including the MMIO space bit where applicable;
- alignment fault: misaligned address;
- software `TRAP`: the zero-extended `imm8` service selector;
- interrupt: zero.

## Interrupt Sources and Priority

The baseline block accepts 16 level-sensitive interrupt inputs. IDs `0` and `1`
are reserved for software and timer interrupts. IDs `2` through `15` are
platform external interrupts 0 through 13.

`IENABLE` masks individual sources and `IPENDING` exposes synchronized pending
levels. An interrupt is eligible when `STATUS.IE = 1` and the corresponding bit
is set in both registers. The numerically lowest eligible ID has highest
priority. Inputs remain pending until their device or interrupt controller
deasserts them; writing `IPENDING` does not acknowledge a device.

Reset is not an interrupt and always has precedence. Non-maskable interrupts
are deferred because they require a second save bank or a double-trap policy.

## Precise Trap Entry

Trap entry occurs at an instruction boundary after all older instructions have
completed and before any younger instruction changes architectural state.

1. Write `EPC`:
   - synchronous fault: address of the faulting instruction;
   - software `TRAP`: address of the following instruction;
   - interrupt: address of the next instruction that would execute.
2. Write `CAUSE` and `TVAL`.
3. Copy `STATUS.IE` to `STATUS.PIE`.
4. Copy `STATUS.MODE` to `STATUS.PMODE`.
5. Clear `STATUS.IE` and set `STATUS.MODE = M`.
6. Cancel any `WFI` state.
7. Redirect execution to `TVEC`.

The first profile uses direct vectoring: every cause enters at `TVEC`, and the
handler dispatches by reading `CAUSE`.

Faulting instructions do not retire. Stores and MMIO operations either complete
before trap entry or have no architectural effect; partial MMIO side effects
must be documented as a platform deviation. `MSI` followed by `MCP` remains two
instructions and an interrupt may occur between them.

## Trap Return and Nesting

`ERET` is Machine-only and performs:

1. `pc = EPC`;
2. `STATUS.MODE = STATUS.PMODE`;
3. `STATUS.IE = STATUS.PIE`;
4. clear `STATUS.PIE` and `STATUS.PMODE`.

The save bank is one level deep. Handlers that re-enable interrupts must first
save `EPC`, `CAUSE`, `TVAL`, and relevant `STATUS` state in ordinary memory.

## Waiting

`WFI` is Machine-only. It may stop instruction issue until an interrupt becomes
pending. A pending interrupt wakes the core even when masked; it is taken only
when eligible. Implementations may resume spuriously, so software must recheck
its condition.

## OASIS-16P Instruction Encoding

OASIS-16P uses Base-16T class `00`, opcode `1110`, as a system group:

| Bits | Field |
| --- | --- |
| `31:30` | class `00` |
| `29:26` | system opcode `1110` |
| `25:22` | `subop` |
| `21:16` | register `ra` |
| `15:8` | `arg8` system-register ID or trap immediate |
| `7:0` | reserved, zero |

| Subop | Instruction | Operation |
| --- | --- | --- |
| `0000` | `TRAP imm8` | Enter Machine mode with software-trap cause |
| `0001` | `ERET` | Return from trap |
| `0010` | `WFI` | Wait for interrupt or resume event |
| `0011` | `CSRR ra, csr8` | Read system register into `ra` |
| `0100` | `CSRW ra, csr8` | Write `ra` to system register |
| `0101` | `CSRS ra, csr8` | Atomically set bits selected by `ra` |
| `0110` | `CSRC ra, csr8` | Atomically clear bits selected by `ra` |

For `TRAP`, `ra` and reserved bits must be zero. For `ERET` and `WFI`, `ra`,
`arg8`, and reserved bits must be zero. Invalid subops raise an illegal-
instruction exception when the extension is present.

## OASIS-32P Mapping

OASIS-32P preserves the same modes, register IDs, causes, entry ordering,
priority, and return behavior. System registers widen to 32 bits. `TRAP` remains
in class `0x0`; `ERET`, `WFI`, and CSR operations use class `0xE`. OASIS-32P
does not reuse OASIS-16P binary encodings.

## Implementation Block Contract

A reusable interrupt/trap/privilege block exposes:

- current privilege mode and global interrupt-enable state;
- 16 synchronized interrupt request inputs;
- synchronous exception request, cause, `TVAL`, and faulting/next PC inputs;
- retired-instruction boundary indication;
- CSR read/write port;
- trap redirect valid/address and pipeline-flush outputs;
- `WFI` wait and wake indications.

The core owns retirement and supplies precise PCs. The block owns system
registers, arbitration, trap-state capture, privilege checks, and redirects.
This boundary is intended to be shared by DungV and DungV-32.
