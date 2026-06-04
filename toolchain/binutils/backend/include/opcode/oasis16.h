#ifndef OASIS16_OPCODE_H
#define OASIS16_OPCODE_H

#include "bfd.h"

enum oasis16_opcode_class
{
  OASIS16_CLASS_TOOL = 0,
  OASIS16_CLASS_ALU = 1,
  OASIS16_CLASS_REG = 2,
  OASIS16_CLASS_MEM = 3
};

enum oasis16_operand_kind
{
  OASIS16_OPERANDS_NONE,
  OASIS16_OPERANDS_RA,
  OASIS16_OPERANDS_RA_RB,
  OASIS16_OPERANDS_RA_IMM6,
  OASIS16_OPERANDS_RA_IMM16,
  OASIS16_OPERANDS_RA_RB_TARGET8,
  OASIS16_OPERANDS_TARGET8,
  OASIS16_OPERANDS_RB,
  OASIS16_OPERANDS_RA_ADDR9,
  OASIS16_OPERANDS_ADDR9_IMM16,
  OASIS16_OPERANDS_RA_MEM_RB_OFF6
};

enum oasis16_reloc_field
{
  OASIS16_RELOC_FIELD_NONE,
  OASIS16_RELOC_FIELD_IMM16,
  OASIS16_RELOC_FIELD_TARGET8,
  OASIS16_RELOC_FIELD_ADDR9,
  OASIS16_RELOC_FIELD_OFF6
};

struct oasis16_opcode
{
  const char *name;
  unsigned int insn_class;
  unsigned int opcode;
  enum oasis16_operand_kind operands;
  const char *format;
};

struct oasis16_insn
{
  unsigned int ra;
  unsigned int rb;
  int immediate;
  int offset;
  int target;
  unsigned int address;
};

extern const struct oasis16_opcode oasis16_opcodes[];
extern const unsigned int oasis16_num_opcodes;

const struct oasis16_opcode *oasis16_lookup_opcode(const char *name);
bfd_boolean oasis16_encode_instruction(const struct oasis16_opcode *opcode,
                                       const struct oasis16_insn *operands,
                                       unsigned int *word);
bfd_boolean oasis16_signed_range(int value, int bits);
bfd_boolean oasis16_unsigned_range(unsigned int value, int bits);

#endif
