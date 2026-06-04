#include "sysdep.h"
#include "opcode/oasis16.h"

const struct oasis16_opcode oasis16_opcodes[] =
{
  { "ADI", 0, 0x1, "ra,imm16" },
  { "SBI", 0, 0x2, "ra,imm16" },
  { "LDR", 0, 0x3, "ra,[rb+off6]" },
  { "STR", 0, 0x4, "ra,[rb+off6]" },
  { "CALL", 0, 0x5, "target8" },
  { "RET", 0, 0x6, "" },
  { "JMR", 0, 0x7, "rb" },
  { "JLT", 0, 0x8, "ra,rb,target8" },
  { "JGE", 0, 0x9, "ra,rb,target8" },
  { "JLTU", 0, 0xa, "ra,rb,target8" },
  { "JGEU", 0, 0xb, "ra,rb,target8" },
  { "ADD", 1, 0x1, "ra,rb" },
  { "SUB", 1, 0x2, "ra,rb" },
  { "AND", 1, 0x3, "ra,rb" },
  { "OOR", 1, 0x4, "ra,rb" },
  { "XOR", 1, 0x5, "ra,rb" },
  { "SHR", 1, 0x6, "ra,imm6" },
  { "SHL", 1, 0x7, "ra,imm6" },
  { "RTR", 1, 0x8, "ra,imm6" },
  { "RTL", 1, 0x9, "ra,imm6" },
  { "NOT", 1, 0xa, "ra" },
  { "MLT", 1, 0xb, "ra,rb" },
  { "JEQ", 1, 0xc, "ra,rb,target8" },
  { "JNE", 1, 0xd, "ra,rb,target8" },
  { "JMP", 1, 0xe, "target8" },
  { "NOP", 1, 0xf, "" },
  { "MVV", 2, 0x2, "ra,rb" },
  { "MVI", 2, 0x3, "ra,imm16" },
  { "MVF", 3, 0x1, "ra,[addr9]" },
  { "MVT", 3, 0x2, "ra,[addr9]" },
  { "MSI", 3, 0x3, "[addr9],imm16" },
};

const unsigned int oasis16_num_opcodes =
  sizeof(oasis16_opcodes) / sizeof(oasis16_opcodes[0]);
