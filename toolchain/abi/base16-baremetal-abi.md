# OASIS Base-16T Bare-Metal ABI Draft

Status: draft ABI used by the current GCC/binutils bring-up.

This ABI records the decisions needed to make C and C++ compilation possible for
the Base-16T toolchain profile.

## Target Names

| Purpose | Name |
| ------- | ---- |
| ISA profile | `oasis-base16t-v1.0` |
| Generic bare-metal target | `oasis16-unknown-elf` |
| GCC/binutils target alias | `oasis16-elf` |

## Register Roles

| Registers | Role | Volatility |
| --------- | ---- | ---------- |
| `r0` | General register, not hardwired zero | Caller-saved |
| `r1` - `r3` | Return values and scratch | Caller-saved |
| `r4` - `r11` | Function arguments | Caller-saved |
| `r12` - `r31` | Temporaries | Caller-saved |
| `r32` - `r55` | Saved registers | Callee-saved |
| `r56` | Stack pointer `sp` | Callee-saved |
| `r57` | Frame pointer `fp` | Callee-saved |
| `r58` | Return address `ra` | Caller-saved |
| `r59` / `sap` | Scratch/far-address pointer | Caller-saved |
| `r60` / `sdata` | Scratch transfer value | Caller-saved |
| `r61` - `r63` | Reserved for toolchain, debug, or platform | Reserved |

## Calling Convention

- Arguments are passed in `r4` through `r11`.
- Additional arguments are passed on the stack.
- Return values are passed in `r1` and `r2`.
- `CALL` stores the return address in `r58`.
- `RET` returns to `r58[7:0]`.
- Stack grows down.
- Stack alignment is 2 bytes.
- Stack slots are 16-bit data-memory words.
- Callers allocate outgoing stack arguments before `CALL` and release them after
  return.
- Callees that need nested calls must save `r58` before issuing another `CALL`.
- Callees must preserve `r32` through `r57` if they modify them.
- `r59` and `r60` are caller-saved ABI temporaries used by far-address and
  staged-transfer expansions.
- `r61` through `r63` must not be used by portable application code.

## C Data Model

The Base-16T C data model is intentionally small and freestanding:

| C type | Size | Alignment | Notes |
| ------ | ---- | --------- | ----- |
| `char` | 16 bits | 1 word | Stored in one data-memory word |
| `short` | 16 bits | 1 word | Same representation as `int` |
| `int` | 16 bits | 1 word | Natural scalar type |
| `long` | 16 bits | 1 word | Initial GCC target model |
| `long long` | 64 bits | 1 word | Compiler/libgcc helper backed |
| pointer | 16 bits | 1 word | `{mmio, addr15}` word address |

Base-16T data memory is word-addressed, so byte addressing is not
architecturally visible. `char` is therefore a 16-bit storage unit in the first
ABI. A future byte-addressed profile may define a different C data model.

## Stack Frame Shape

A conventional non-leaf frame should use this high-level layout:

```text
higher addresses
  incoming stack arguments
  caller frame
  saved return address, when needed
  saved frame pointer, when used
  saved callee-saved registers
  local variables and spills
lower addresses
```

Recommended prologue for a function that needs a frame:

```asm
SBI r56, frame_words
STR r58, [r56 + ra_slot]
STR r57, [r56 + fp_slot]
MVV r57, r56
```

Recommended epilogue:

```asm
LDR r58, [r56 + ra_slot]
LDR r57, [r56 + fp_slot]
ADI r56, frame_words
RET
```

Leaf functions may omit the frame pointer and return-address save when they do
not need stack locals, spills, alloca-like storage, or nested calls.

## Required ISA Mechanisms

Base-16T defines the instructions required by this ABI:

| Need | Base-16T mechanism |
| ---- | ------------------ |
| Stack adjustment | `ADI`, `SBI` |
| Stack-relative load/store | `LDR`, `STR` with base register `r56` |
| Function call | `CALL target8` |
| Function return | `RET` |
| Indirect branch | `JMR rb` |
| Signed comparisons | `JLT`, `JGE` |
| Unsigned comparisons | `JLTU`, `JGEU` |

The first GCC backend should target Base-16T, not Base-16.

## C++ Freestanding ABI

Base-16T C++ support is freestanding and intentionally minimal. The v0.2
baseline documents the symbols and helper hooks needed for early compile/link
support; hosted C++ and full constructor/destructor startup policy remain
outside the required baseline.

| Feature | ABI expectation |
| ------- | --------------- |
| Name mangling | Use the Itanium C++ ABI mangling where practical |
| `this` pointer | Passed as the first argument in `r4` |
| Return values | Same as C: `r1` and `r2` |
| Constructors | Normal functions using the C calling convention |
| Destructors | Normal functions using the C calling convention |
| Static constructors | Init-array range symbols are provided; startup invocation is platform/runtime policy |
| Static destructors | Fini-array range symbols are provided; invocation is optional platform/runtime policy |
| `new`/`delete` | Weak runtime hooks or unavailable unless a heap provider is linked |
| Exceptions | Disabled in the first ABI; compile with no exception unwinding |
| RTTI | Optional; disabled by default in the first ABI |
| Guard variables | Helper hooks are provided for function-local statics |

The first C++ toolchain should assume these defaults:

```text
-fno-exceptions
-fno-rtti
freestanding runtime
no hosted standard library
```

Required runtime symbols for C++ bring-up:

| Symbol | Purpose |
| ------ | ------- |
| `__oasis_init_array_start` | first static constructor entry |
| `__oasis_init_array_end` | one past the last static constructor entry |
| `__oasis_fini_array_start` | first static destructor entry, optional |
| `__oasis_fini_array_end` | one past the last static destructor entry, optional |
| `__cxa_pure_virtual` | abort hook for pure virtual calls |
| `__cxa_guard_acquire` | local static guard acquire |
| `__cxa_guard_release` | local static guard release |
| `__cxa_guard_abort` | local static guard abort |
| `operator new` / `operator delete` | weak allocation hooks when heap support exists |

The default OASIS startup object does not currently walk `.init_array` or
`.fini_array`. Implementations that need global constructor/destructor execution
must provide a platform startup layer that iterates the exported ranges before
and after `main`, respectively.

If an implementation does not provide a heap, `operator new` should fail by
parking in `__oasis_abort` or by returning according to the selected C++ runtime
policy. The default OASIS runtime remains heapless until an implementation
advertises a memory provider.

## Memory Map

| Region | Addressing | Purpose |
| ------ | ---------- | ------- |
| Instruction memory | 8-bit instruction index | Program text |
| Data memory low words | 12-bit word index | Globals, static data, MMIO |
| Data memory high words | 12-bit word index | Stack |

The default linker script uses a 256-instruction text memory and 4096-word data
memory. Implementations may override the memory map while keeping ABI register
roles stable.

## External Memory And MMIO ABI Hooks

Base-16T keeps the architectural address type at 16 bits. Bit 15 selects
ordinary memory (`0`) or MMIO (`1`); bits 14:0 select a word within that space.
A core or SoC may attach external memory behind part of the ordinary-memory
space, but portable software must discover or be linked for that map explicitly.

The default ABI reserves ordinary-memory words `0x0000` through `0x001f` as a
32-word scratch block. A platform may override the reservation, including its
size and location, through its linker script. The corresponding MMIO addresses
are not reserved.

Expected linker symbols for implementations with external memory:

| Symbol | Purpose |
| ------ | ------- |
| `__oasis_extmem_start` | first external data-memory word |
| `__oasis_extmem_end` | one past the last external data-memory word |
| `__oasis_heap_start` | first heap word, if heap is available |
| `__oasis_heap_end` | one past the last heap word |
| `__oasis_stack_top` | initial stack pointer value |
| `__oasis_scratch_start` | first reserved ordinary-memory scratch word |
| `__oasis_scratch_end` | one past the final scratch word |
| `__oasis_scratch_words` | number of reserved scratch words |

An external-memory implementation may use memory-mapped control registers or an
optional extension instruction profile. The C/C++ ABI should interact with it
through the linker map, runtime startup, and implementation headers rather than
assuming dedicated opcodes.

## Function Example

```asm
; unsigned add(unsigned a, unsigned b)
; a in r4, b in r5, return in r1
MVV r1, r4
ADD r1, r5
RET
```
