# OASIS-32 Memory Model

Status: experimental planning draft.

OASIS-32 is byte addressed. Architectural addresses are 32 bits wide.

## Address Spaces

| Property | Draft Rule |
| -------- | ---------- |
| Address width | 32 bits |
| Address unit | byte |
| Ordinary-memory space | 4 GiB |
| MMIO space | 4 GiB |
| Physical memory size | implementation-defined in Base-32 |

A compliant Base-32 implementation may expose less than 4 GiB in either space.
The spaces do not alias: the same numeric address may identify an ordinary byte
and an MMIO register. Accesses outside an implemented region are
implementation-defined in Base-32. Privileged profiles should define faults.

Every OASIS-32 memory instruction explicitly selects ordinary memory or MMIO
through the `space` bit in the M-format `space_size_flags` field. Registers and
offsets retain their full 32-bit address width; OASIS-32 does not encode the
space selector by reducing an address field as Base-16 does.

Assembly uses the same explicit `mem:` and `io:` spelling established by
OASIS-16 v1.0. Compiler IR and relocations must preserve the address-space
distinction rather than infer MMIO from a numeric range.

## Scratch And Staged Transfers

OASIS-32 inherits the explicit staged-transfer contract but does not require a
baseline scratch reservation. Its full-width immediate and memory formats
should lower far stores without the Base-16 `addr11` workaround. Platforms may
publish scratch memory for DMA, inter-core, or peripheral protocols, but that is
a platform ABI feature.

If an OASIS-32 `MCP` form is standardized, it must explicitly identify source
and destination spaces, preserve program order, and define faults between its
read and write. It must not depend on hidden state from a preceding instruction.

## Load And Store Sizes

| Mnemonic | Meaning |
| -------- | ------- |
| `LDB` | load byte, zero-extend |
| `LDBS` | load byte, sign-extend |
| `LDH` | load 16-bit halfword, zero-extend |
| `LDHS` | load 16-bit halfword, sign-extend |
| `LDW` | load 32-bit word |
| `STB` | store byte |
| `STH` | store 16-bit halfword |
| `STW` | store 32-bit word |

## Alignment

| Access | Alignment |
| ------ | --------- |
| byte | any address |
| halfword | 2-byte aligned |
| word | 4-byte aligned |

Misaligned halfword and word access is illegal in Base-32. Future profiles may
define implementation support for misaligned access.

## Caches

Base-32 does not expose cache behavior architecturally. Cache maintenance,
memory protection, and memory ordering beyond normal program order are reserved
for future privileged or atomic extensions.
