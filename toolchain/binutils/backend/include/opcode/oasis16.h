#ifndef OASIS16_OPCODE_H
#define OASIS16_OPCODE_H

enum oasis16_opcode_class
{
  OASIS16_CLASS_TOOL = 0,
  OASIS16_CLASS_ALU = 1,
  OASIS16_CLASS_REG = 2,
  OASIS16_CLASS_MEM = 3
};

struct oasis16_opcode
{
  const char *name;
  unsigned int insn_class;
  unsigned int opcode;
  const char *format;
};

extern const struct oasis16_opcode oasis16_opcodes[];
extern const unsigned int oasis16_num_opcodes;

#endif
