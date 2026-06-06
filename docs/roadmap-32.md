# OASIS-32 / 64-bit Instruction Architecture Planning

## Goal

Design OASIS-32 as the next architectural profile after OASIS v0.1 Base-16/Base-16T.

OASIS-32 should introduce:

- 32-bit data path
- 32-bit general-purpose registers
- 32-bit byte-addressed memory space
- 64-bit fixed-width instruction encoding
- Expanded instruction classes
- Better compiler friendliness
- Cleaner immediate handling
- Extension space for future privileged, memory, SIMD, DSP, or system features

The goal is not to replace OASIS-16, but to define a larger profile:

```text
Base-16   = compact learning / FPGA profile
Base-16T  = compiler-oriented 16-bit profile
Base-32   = 32-bit general-purpose profile
Base-32T  = compiler/toolchain-oriented 32-bit profile
```

---

# Strategic Move 1: Preserve the OASIS Design Philosophy

OASIS-32 should remain:

```text
simple
implementation-friendly
well-documented
easy to decode
FPGA-friendly
toolchain-friendly
```

Avoid copying RISC-V, ARM, MIPS, or OpenRISC directly.

OASIS should have its own identity:

```text
wide, regular instructions
simple decode
explicit operation classes
large immediate capacity
clean extension space
```

---

# Strategic Move 2: Use a Fixed 64-bit Instruction Width

For OASIS-32, use fixed-width 64-bit instructions.

Benefits:

- Very simple decode
- Plenty of room for register fields
- Large immediates
- Clean instruction classes
- Fewer compressed or extended encoding hacks
- Easier compiler backend work
- Easier disassembler and assembler work

Cost:

- Larger program memory footprint
- More instruction fetch bandwidth required

This is acceptable because OASIS-32 should prioritize clarity, compiler friendliness, and hardware simplicity.

---

# Strategic Move 3: Define a Universal 64-bit Header

Every OASIS-32 instruction should share a common top-level format.

Suggested high-level layout:

```text
63        60 59        56 55        48 47        40 39        32 31                  0
+------------+------------+------------+------------+------------+----------------------+
| class[3:0] | op[3:0]    | rd[7:0]    | ra[7:0]    | rb[7:0]    | imm/func/extra[31:0] |
+------------+------------+------------+------------+------------+----------------------+
```

This gives:

```text
16 instruction classes
16 primary ops per class
256 architectural register encodings
32-bit immediate/extra field
```

Even if OASIS-32 initially exposes only 64 registers, use 8-bit register fields now to avoid future encoding pressure.

---

# Strategic Move 4: Define Register Strategy Early

Recommended OASIS-32 register model:

```text
r0-r63     general-purpose registers
r0         hardwired zero, strongly recommended
sp         stack pointer alias
fp         frame pointer alias
ra         return address alias
rv         return value alias
```

Possible ABI aliases:

```text
r0   zero
r1   ra
r2   sp
r3   fp
r4   rv0
r5   rv1
r6-r15   argument registers
r16-r31  caller-saved temporaries
r32-r47  callee-saved registers
r48-r63  reserved / platform / extension
```

Keep architectural register fields 8 bits wide even if only 64 are legal in Base-32.

Reserved register IDs:

```text
64-255 reserved for future profiles
```

---

# Strategic Move 5: Make OASIS-32 Byte Addressed

OASIS-16 currently uses word-addressed memory.

OASIS-32 should move to byte-addressed memory:

```text
32-bit address
4 GiB architectural address space
```

Define load/store sizes explicitly:

```text
LDB   load byte unsigned
LDBS  load byte signed
LDH   load halfword unsigned
LDHS  load halfword signed
LDW   load 32-bit word

STB   store byte
STH   store halfword
STW   store word
```

Initial alignment rule:

```text
LDH/STH require 2-byte alignment
LDW/STW require 4-byte alignment
misaligned access is illegal in Base-32
```

Later profiles may allow misaligned access.

---

# Strategic Move 6: Define Instruction Classes

Use the 4-bit `class` field as the top-level decoder.

Suggested class map:

```text
0x0  SYSTEM / SPECIAL
0x1  INTEGER ALU
0x2  INTEGER ALU IMMEDIATE
0x3  SHIFT / BIT MANIPULATION
0x4  LOAD
0x5  STORE
0x6  BRANCH
0x7  JUMP / CALL
0x8  COMPARE / SET
0x9  MOVE / CONSTANT
0xA  MULTIPLY / DIVIDE
0xB  ATOMIC / MEMORY ORDERING
0xC  COPROCESSOR / CUSTOM
0xD  VECTOR / SIMD RESERVED
0xE  PRIVILEGED RESERVED
0xF  EXTENDED / ESCAPE
```

Do not implement every class immediately.

Reserve them now so the ISA has room to grow.

---

# Strategic Move 7: Define a Few Standard Encoding Formats

Even with 64-bit fixed instructions, avoid one-off encodings.

Use a small set of canonical formats.

## R-Type

Register-register operations.

```text
63:60 class
59:56 op
55:48 rd
47:40 ra
39:32 rb
31:24 rc / func
23:0  reserved / func / flags
```

Example:

```asm
ADD r3, r1, r2
```

Operation:

```text
r3 = r1 + r2
```

## I-Type

Register-immediate operations.

```text
63:60 class
59:56 op
55:48 rd
47:40 ra
39:32 subop / flags
31:0  imm32
```

Example:

```asm
ADDI r3, r1, 100
```

Operation:

```text
r3 = r1 + sign_extend(imm32)
```

## M-Type

Memory operations.

```text
63:60 class
59:56 op
55:48 rd_or_rs
47:40 base
39:32 mode / size / flags
31:0  signed_offset
```

Example:

```asm
LDW r3, [r1 + 16]
STW r3, [r1 - 8]
```

## B-Type

Conditional branches.

```text
63:60 class
59:56 condition
55:48 ra
47:40 rb
39:32 flags
31:0  signed_pc_relative_offset
```

Example:

```asm
BEQ r1, r2, label
BLT r1, r2, label
BLTU r1, r2, label
```

## J-Type

Jump and call operations.

```text
63:60 class
59:56 op
55:48 rd / link register
47:40 base register
39:32 flags
31:0  signed_offset / absolute target
```

Example:

```asm
CALL label
JMP label
JALR r1
RET
```

## U-Type

Large constant construction.

```text
63:60 class
59:56 op
55:48 rd
47:32 flags/subop
31:0  immediate
```

Example:

```asm
LUI r1, 0x12345678
ORI r1, r1, 0xABCD
```

---

# Strategic Move 8: Make Immediate Handling a Strength

A 64-bit instruction gives OASIS-32 room for large immediates.

Support these from the start:

```text
ADDI rd, ra, imm32
ANDI rd, ra, imm32
ORI  rd, ra, imm32
XORI rd, ra, imm32
LDW  rd, [ra + imm32]
STW  rs, [ra + imm32]
BEQ  ra, rb, pc_rel32
CALL pc_rel32
```

This makes compiler output easier and reduces constant-loading instruction count.

For full 32-bit constants:

```asm
MVI r1, 0x12345678
```

should be valid and encode directly.

For future 64-bit profile compatibility:

```asm
LUI
ORI
MOVHI
MOVLO
```

can still exist, but OASIS-32 should not require awkward multi-instruction constant loading for normal 32-bit values.

---

# Strategic Move 9: Add Toolchain-Oriented Operations Early

Base-32T should include compiler-critical instructions from the beginning:

```text
ADD
SUB
AND
OR
XOR
NOT
NEG
ADDI
ANDI
ORI
XORI
SHL
SHR
SAR
MUL
DIV
DIVU
MOD
MODU
LD/ST byte
LD/ST halfword
LD/ST word
CALL
RET
JMP
JALR
BEQ
BNE
BLT
BLE
BGT
BGE
BLTU
BLEU
BGTU
BGEU
```

Also include:

```text
SLT
SLTU
SEQ
SNE
```

These make C comparison lowering easier.

---

# Strategic Move 10: Decide Flagless vs Flag-Based Now

OASIS-16 has no status flags.

Recommendation:

```text
Keep OASIS-32 flagless.
```

Use explicit compare/branch or register comparison branches:

```asm
BEQ r1, r2, label
BLT r1, r2, label
SLT r3, r1, r2
```

Benefits:

- Easier pipelining
- Fewer hidden dependencies
- Cleaner compiler backend
- Simpler out-of-order future possibility
- Easier formal verification

Avoid condition-code flags unless a future optional extension needs them.

---

# Strategic Move 11: Reserve Extension Space Formally

Create extension namespaces:

```text
OASIS-32I   base integer
OASIS-32T   compiler/toolchain support
OASIS-32M   multiply/divide
OASIS-32A   atomics
OASIS-32P   privileged/system
OASIS-32V   vector/SIMD
OASIS-32C   custom/vendor
```

Document extension rules:

```text
Reserved opcodes must trap or be treated as illegal.
Custom opcodes must live only in class 0xC unless formally standardized.
Experimental opcodes must be marked unstable.
```

---

# Strategic Move 12: Define Illegal Instruction Behavior

OASIS-32 should define illegal instructions clearly.

For the first non-privileged profile:

```text
An illegal instruction halts the core or enters implementation-defined trap behavior.
```

For future privileged profile:

```text
An illegal instruction raises an illegal-instruction exception.
```

For DungV-style simple cores:

```text
illegal instruction -> halt/error output
```

This avoids undefined behavior.

---

# Strategic Move 13: Define Memory System Compatibility

OASIS-32 should architecturally expose:

```text
32-bit byte-addressed memory
```

But implementations may support smaller physical memory.

Document:

```text
A compliant OASIS-32 core may implement less than 4 GiB of physical RAM.
Addresses outside implemented memory are implementation-defined in Base-32.
Privileged profiles should define memory faults.
```

Prepare for caches but do not expose them in the base ISA:

```text
L1/L2 cache behavior is implementation-level.
Cache maintenance instructions are reserved for OASIS-32P.
```

---

# Strategic Move 14: Keep Decode FPGA-Friendly

Use fixed field locations:

```text
class always at 63:60
op always at 59:56
rd always at 55:48
ra always at 47:40
rb/base always at 39:32
immediate/extra always at 31:0
```

Avoid encodings where the same bits mean wildly different things.

Use `class + op` as the primary decode key.

This makes RTL decode look like:

```verilog
case (instr[63:60])
  CLASS_ALU:    decode_alu();
  CLASS_ALUI:   decode_alu_imm();
  CLASS_LOAD:   decode_load();
  CLASS_STORE:  decode_store();
  CLASS_BRANCH: decode_branch();
  CLASS_JUMP:   decode_jump();
endcase
```

---

# Strategic Move 15: Create Machine-Readable Encoding Tables First

Before writing RTL, create:

```text
tables/oasis32/opcode-map.csv
tables/oasis32/encoding-formats.csv
tables/oasis32/registers.csv
tables/oasis32/extensions.csv
```

Then generate:

```text
instruction docs
assembler opcode tables
disassembler tables
RTL constants
Python emulator constants
compliance test templates
```

Codex task:

```text
Do not hand-maintain duplicate opcode definitions.
Use tables as the source of truth.
```

---

# Strategic Move 16: Add an OASIS-32 Reference Emulator Before RTL

Create:

```text
tools/oasis32_emulator.py
```

The emulator should support:

```text
register file
PC
byte-addressed memory
instruction decode
instruction execution
illegal instruction handling
```

Then every instruction should have compliance tests.

Flow:

```text
assembly
 -> assembler
 -> binary
 -> emulator
 -> expected registers/memory/PC
```

Only after this should RTL begin.

---

# Strategic Move 17: Define OASIS-32 Documentation Layout

Add:

```text
spec/oasis-v0.2-draft.md
spec/oasis32/overview.md
spec/oasis32/encoding.md
spec/oasis32/registers.md
spec/oasis32/memory.md
spec/oasis32/instruction-classes.md
spec/oasis32/abi.md
spec/oasis32/extensions.md
spec/oasis32/compliance.md
```

Add instruction pages under:

```text
instructions/oasis32/
```

Example:

```text
instructions/oasis32/add.md
instructions/oasis32/addi.md
instructions/oasis32/ldw.md
instructions/oasis32/stw.md
instructions/oasis32/beq.md
```

---

# Strategic Move 18: Define ABI Early

Base-32T should define a minimal C ABI:

```text
int      32-bit
short    16-bit
char     8-bit
pointer  32-bit
long     32-bit initially
long long optional/compiler-emulated
```

Stack:

```text
stack grows downward
sp must be 4-byte aligned
function arguments passed in registers first
extra arguments passed on stack
return value in rv0
return address in ra
```

This is essential for GCC/LLVM work.

---

# Strategic Move 19: Plan the RTL Around the Encoding

Recommended first OASIS-32 core pipeline:

```text
IF  instruction fetch
ID  decode/register read
EX  execute/address generation
MEM memory access
WB  writeback
```

Memory interface:

```text
mem_valid
mem_ready
mem_addr[31:0]
mem_wdata[31:0]
mem_rdata[31:0]
mem_write
mem_size[1:0]
```

Instruction fetch interface:

```text
imem_valid
imem_ready
imem_addr[31:0]
imem_rdata[63:0]
```

The core should support stalling from day one.

---

# Strategic Move 20: Define Milestones

## Milestone A: OASIS-32 Encoding Draft

Deliver:

```text
64-bit instruction format
class map
register map
memory model
initial opcode table
```

## Milestone B: Machine-Readable Tables

Deliver:

```text
CSV/JSON/YAML opcode tables
generated docs
validation script
```

## Milestone C: Assembler Support

Deliver:

```text
oasis-asm --profile oasis32
```

## Milestone D: Emulator Support

Deliver:

```text
oasis32_emulator.py
```

## Milestone E: Compliance Tests

Deliver tests for:

```text
ALU
immediates
loads/stores
branches
calls
ABI basics
```

## Milestone F: Minimal RTL Core

Deliver:

```text
fetch
decode
register file
ALU
load/store unit
branch unit
writeback
```

## Milestone G: Toolchain Planning

Deliver:

```text
oasis32-unknown-elf target notes
GCC backend deltas from oasis16
ABI document
crt0
linker script
```

---

# First Codex Task

Implement the OASIS-32 planning scaffold without changing OASIS v0.1.

Create:

```text
spec/oasis-v0.2-draft.md
spec/oasis32/overview.md
spec/oasis32/encoding.md
spec/oasis32/registers.md
spec/oasis32/memory.md
spec/oasis32/instruction-classes.md
spec/oasis32/abi.md
spec/oasis32/extensions.md
tables/oasis32/opcode-map.csv
tables/oasis32/encoding-formats.csv
```

Add validation tooling:

```text
tools/validate_oasis32_tables.py
```

Add README note:

```text
OASIS v0.2-draft is experimental and does not modify OASIS v0.1 compatibility.
```

Do not implement RTL yet.

Do not modify Base-16/Base-16T instruction semantics.

The first goal is to make OASIS-32 a documented architecture contract before implementation work begins.

## Initial Scaffold Status

Implemented in the first OASIS-32 planning pass:

- `spec/oasis-v0.2-draft.md`
- `spec/oasis32/overview.md`
- `spec/oasis32/encoding.md`
- `spec/oasis32/registers.md`
- `spec/oasis32/memory.md`
- `spec/oasis32/instruction-classes.md`
- `spec/oasis32/abi.md`
- `spec/oasis32/extensions.md`
- `spec/oasis32/compliance.md`
- `toolchain/abi/base32-baremetal-abi.md`
- `tables/oasis32/opcode-map.csv`
- `tables/oasis32/encoding-formats.csv`
- `tables/oasis32/registers.csv`
- `tables/oasis32/extensions.csv`
- `tools/validate_oasis32_tables.py`

The validator is wired into `make check`. This keeps OASIS-32 draft table work
visible while preserving OASIS v0.1 Base-16/Base-16T compatibility.
