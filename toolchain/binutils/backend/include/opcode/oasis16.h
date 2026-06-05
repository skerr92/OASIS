#ifndef OASIS16_OPCODE_H
#define OASIS16_OPCODE_H

#include "bfd.h"
#include "dis-asm.h"

#define OASIS16_INSN_SIZE 4
#define OASIS16_REG_COUNT 64
#define OASIS16_CLASS_SHIFT 30
#define OASIS16_TOOL_OPCODE_SHIFT 26
#define OASIS16_ALU_OPCODE_SHIFT 26
#define OASIS16_REG_OPCODE_SHIFT 28
#define OASIS16_MEM_OPCODE_SHIFT 28
#define OASIS16_RA_TOOL_SHIFT 20
#define OASIS16_RA_ALU_SHIFT 20
#define OASIS16_RA_REG_SHIFT 22
#define OASIS16_RA_MEM_SHIFT 22
#define OASIS16_RB_TOOL_SHIFT 14
#define OASIS16_RB_ALU_SHIFT 14
#define OASIS16_RB_REG_SHIFT 16
#define OASIS16_TARGET8_SHIFT 6
#define OASIS16_ADDR9_SHIFT 13
#define OASIS16_MSI_ADDR9_SHIFT 19
#define OASIS16_OFF6_SHIFT 8
#define OASIS16_CLASS_MASK 0x3u
#define OASIS16_OPCODE4_MASK 0xfu
#define OASIS16_OPCODE2_MASK 0x3u
#define OASIS16_REG_MASK 0x3fu
#define OASIS16_IMM6_MASK 0x3fu
#define OASIS16_IMM16_MASK 0xffffu
#define OASIS16_TARGET8_MASK 0xffu
#define OASIS16_ADDR9_MASK 0x1ffu

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
bool oasis16_encode_instruction(const struct oasis16_opcode *opcode,
                                const struct oasis16_insn *operands,
                                unsigned int *word);
bool oasis16_decode_instruction(unsigned int word,
                                const struct oasis16_opcode **opcode,
                                struct oasis16_insn *operands);
void oasis16_print_instruction(const struct oasis16_opcode *opcode,
                               const struct oasis16_insn *operands,
                               fprintf_ftype fprintf_func,
                               void *stream);
int print_insn_oasis16(bfd_vma memaddr, struct disassemble_info *info);
bool oasis16_signed_range(int value, int bits);
bool oasis16_unsigned_range(unsigned int value, int bits);

#endif
