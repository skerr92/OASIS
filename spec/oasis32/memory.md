# OASIS-32 Memory Model

Status: experimental planning draft.

OASIS-32 is byte addressed. Architectural addresses are 32 bits wide.

## Address Space

| Property | Draft Rule |
| -------- | ---------- |
| Address width | 32 bits |
| Address unit | byte |
| Architectural space | 4 GiB |
| Physical memory size | implementation-defined in Base-32 |

A compliant Base-32 implementation may expose less than 4 GiB of physical memory.
Accesses outside implemented memory are implementation-defined in Base-32.
Privileged profiles should define memory faults.

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
