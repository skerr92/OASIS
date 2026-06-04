#include "sysdep.h"
#include "opcode/oasis16.h"

const struct oasis16_opcode oasis16_opcodes[] =
{
  { "ADI", 0, 0x1, OASIS16_OPERANDS_RA_IMM16, "ra,imm16" },
  { "SBI", 0, 0x2, OASIS16_OPERANDS_RA_IMM16, "ra,imm16" },
  { "LDR", 0, 0x3, OASIS16_OPERANDS_RA_MEM_RB_OFF6, "ra,[rb+off6]" },
  { "STR", 0, 0x4, OASIS16_OPERANDS_RA_MEM_RB_OFF6, "ra,[rb+off6]" },
  { "CALL", 0, 0x5, OASIS16_OPERANDS_TARGET8, "target8" },
  { "RET", 0, 0x6, OASIS16_OPERANDS_NONE, "" },
  { "JMR", 0, 0x7, OASIS16_OPERANDS_RB, "rb" },
  { "JLT", 0, 0x8, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "JGE", 0, 0x9, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "JLTU", 0, 0xa, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "JGEU", 0, 0xb, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "ADD", 1, 0x1, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "SUB", 1, 0x2, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "AND", 1, 0x3, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "OOR", 1, 0x4, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "XOR", 1, 0x5, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "SHR", 1, 0x6, OASIS16_OPERANDS_RA_IMM6, "ra,imm6" },
  { "SHL", 1, 0x7, OASIS16_OPERANDS_RA_IMM6, "ra,imm6" },
  { "RTR", 1, 0x8, OASIS16_OPERANDS_RA_IMM6, "ra,imm6" },
  { "RTL", 1, 0x9, OASIS16_OPERANDS_RA_IMM6, "ra,imm6" },
  { "NOT", 1, 0xa, OASIS16_OPERANDS_RA, "ra" },
  { "MLT", 1, 0xb, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "JEQ", 1, 0xc, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "JNE", 1, 0xd, OASIS16_OPERANDS_RA_RB_TARGET8, "ra,rb,target8" },
  { "JMP", 1, 0xe, OASIS16_OPERANDS_TARGET8, "target8" },
  { "NOP", 1, 0xf, OASIS16_OPERANDS_NONE, "" },
  { "MVV", 2, 0x2, OASIS16_OPERANDS_RA_RB, "ra,rb" },
  { "MVI", 2, 0x3, OASIS16_OPERANDS_RA_IMM16, "ra,imm16" },
  { "MVF", 3, 0x1, OASIS16_OPERANDS_RA_ADDR9, "ra,[addr9]" },
  { "MVT", 3, 0x2, OASIS16_OPERANDS_RA_ADDR9, "ra,[addr9]" },
  { "MSI", 3, 0x3, OASIS16_OPERANDS_ADDR9_IMM16, "[addr9],imm16" },
};

const unsigned int oasis16_num_opcodes =
  sizeof(oasis16_opcodes) / sizeof(oasis16_opcodes[0]);

bfd_boolean
oasis16_signed_range(int value, int bits)
{
  int min = -(1 << (bits - 1));
  int max = (1 << (bits - 1)) - 1;
  return value >= min && value <= max;
}

bfd_boolean
oasis16_unsigned_range(unsigned int value, int bits)
{
  return value < (1u << bits);
}

const struct oasis16_opcode *
oasis16_lookup_opcode(const char *name)
{
  unsigned int i;

  for (i = 0; i < oasis16_num_opcodes; i++)
    if (strcasecmp(name, oasis16_opcodes[i].name) == 0)
      return &oasis16_opcodes[i];

  return NULL;
}

bfd_boolean
oasis16_encode_instruction(const struct oasis16_opcode *opcode,
                           const struct oasis16_insn *operands,
                           unsigned int *word)
{
  unsigned int encoded = (opcode->insn_class << 30) | (opcode->opcode << 26);

  switch (opcode->operands)
    {
    case OASIS16_OPERANDS_NONE:
      break;

    case OASIS16_OPERANDS_RA:
      if (!oasis16_unsigned_range(operands->ra, 6))
        return FALSE;
      encoded |= operands->ra << 20;
      break;

    case OASIS16_OPERANDS_RA_RB:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6))
        return FALSE;
      if (opcode->insn_class == OASIS16_CLASS_REG)
        encoded |= (operands->ra << 22) | (operands->rb << 16);
      else
        encoded |= (operands->ra << 20) | (operands->rb << 14);
      break;

    case OASIS16_OPERANDS_RA_IMM6:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 6))
        return FALSE;
      encoded |= (operands->ra << 20) | ((unsigned int) operands->immediate << 14);
      break;

    case OASIS16_OPERANDS_RA_IMM16:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 16))
        return FALSE;
      if (opcode->insn_class == OASIS16_CLASS_REG)
        encoded |= (operands->ra << 22) | ((unsigned int) operands->immediate & 0xffff);
      else
        encoded |= (operands->ra << 20) | ((unsigned int) operands->immediate & 0xffff);
      break;

    case OASIS16_OPERANDS_RA_RB_TARGET8:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6)
          || !oasis16_unsigned_range((unsigned int) operands->target, 8))
        return FALSE;
      encoded |= (operands->ra << 20) | (operands->rb << 14)
                 | (((unsigned int) operands->target & 0xff) << 6);
      break;

    case OASIS16_OPERANDS_TARGET8:
      if (!oasis16_unsigned_range((unsigned int) operands->target, 8))
        return FALSE;
      encoded |= ((unsigned int) operands->target & 0xff) << 6;
      break;

    case OASIS16_OPERANDS_RB:
      if (!oasis16_unsigned_range(operands->rb, 6))
        return FALSE;
      encoded |= operands->rb << 14;
      break;

    case OASIS16_OPERANDS_RA_ADDR9:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->address, 9))
        return FALSE;
      encoded |= (operands->ra << 22) | (operands->address << 13);
      break;

    case OASIS16_OPERANDS_ADDR9_IMM16:
      if (!oasis16_unsigned_range(operands->address, 9)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 16))
        return FALSE;
      encoded |= (operands->address << 19)
                 | ((unsigned int) operands->immediate & 0xffff);
      break;

    case OASIS16_OPERANDS_RA_MEM_RB_OFF6:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6)
          || !oasis16_signed_range(operands->offset, 6))
        return FALSE;
      encoded |= (operands->ra << 20) | (operands->rb << 14)
                 | (((unsigned int) operands->offset & 0x3f) << 8);
      break;
    }

  *word = encoded;
  return TRUE;
}
