#include "sysdep.h"
#include "opcode/oasis16.h"

static int
oasis16_sign_extend(unsigned int value, unsigned int bits)
{
  unsigned int sign = 1u << (bits - 1);
  unsigned int mask = (1u << bits) - 1u;

  value &= mask;
  return (int) ((value ^ sign) - sign);
}

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
  { "MCP", 0, 0xc, OASIS16_OPERANDS_RB_SCRATCH11, "[rb],mem:[scratch11]" },
  { "TRAP", 0, 0xe, OASIS16_OPERANDS_TRAP_IMM8, "imm8", 0x0 },
  { "ERET", 0, 0xe, OASIS16_OPERANDS_NONE, "", 0x1 },
  { "WFI", 0, 0xe, OASIS16_OPERANDS_NONE, "", 0x2 },
  { "CSRR", 0, 0xe, OASIS16_OPERANDS_RA_CSR8, "ra,csr8", 0x3 },
  { "CSRW", 0, 0xe, OASIS16_OPERANDS_RA_CSR8, "ra,csr8", 0x4 },
  { "CSRS", 0, 0xe, OASIS16_OPERANDS_RA_CSR8, "ra,csr8", 0x5 },
  { "CSRC", 0, 0xe, OASIS16_OPERANDS_RA_CSR8, "ra,csr8", 0x6 },
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
  { "MVF", 3, 0x1, OASIS16_OPERANDS_RA_SPACE_ADDR11, "ra,space:[addr11]" },
  { "MVT", 3, 0x2, OASIS16_OPERANDS_RA_SPACE_ADDR11, "ra,space:[addr11]" },
  { "MSI", 3, 0x3, OASIS16_OPERANDS_SPACE_ADDR11_IMM16, "space:[addr11],imm16" },
};

const unsigned int oasis16_num_opcodes =
  sizeof(oasis16_opcodes) / sizeof(oasis16_opcodes[0]);

bool
oasis16_signed_range(int value, int bits)
{
  int min = -(1 << (bits - 1));
  int max = (1 << (bits - 1)) - 1;
  return value >= min && value <= max;
}

bool
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

bool
oasis16_encode_instruction(const struct oasis16_opcode *opcode,
                           const struct oasis16_insn *operands,
                           unsigned int *word)
{
  unsigned int encoded = opcode->insn_class << OASIS16_CLASS_SHIFT;

  if (opcode->insn_class == OASIS16_CLASS_REG
      || opcode->insn_class == OASIS16_CLASS_MEM)
    encoded |= opcode->opcode << OASIS16_REG_OPCODE_SHIFT;
  else
    encoded |= opcode->opcode << OASIS16_ALU_OPCODE_SHIFT;

  if (opcode->insn_class == OASIS16_CLASS_TOOL && opcode->opcode == 0xe)
    encoded |= opcode->subopcode << OASIS16_SYSTEM_SUBOP_SHIFT;

  switch (opcode->operands)
    {
    case OASIS16_OPERANDS_NONE:
      break;

    case OASIS16_OPERANDS_RA:
      if (!oasis16_unsigned_range(operands->ra, 6))
        return false;
      encoded |= operands->ra << 20;
      break;

    case OASIS16_OPERANDS_RA_RB:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6))
        return false;
      if (opcode->insn_class == OASIS16_CLASS_REG)
        encoded |= (operands->ra << 22) | (operands->rb << 16);
      else
        encoded |= (operands->ra << 20) | (operands->rb << 14);
      break;

    case OASIS16_OPERANDS_RA_IMM6:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 6))
        return false;
      encoded |= (operands->ra << 20) | ((unsigned int) operands->immediate << 14);
      break;

    case OASIS16_OPERANDS_RA_IMM16:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 16))
        return false;
      if (opcode->insn_class == OASIS16_CLASS_REG)
        encoded |= (operands->ra << 22) | ((unsigned int) operands->immediate & 0xffff);
      else
        encoded |= (operands->ra << 20) | ((unsigned int) operands->immediate & 0xffff);
      break;

    case OASIS16_OPERANDS_RA_RB_TARGET8:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6)
          || !oasis16_unsigned_range((unsigned int) operands->target, 8))
        return false;
      encoded |= (operands->ra << 20) | (operands->rb << 14)
                 | (((unsigned int) operands->target & 0xff) << 6);
      break;

    case OASIS16_OPERANDS_TARGET8:
      if (!oasis16_unsigned_range((unsigned int) operands->target, 8))
        return false;
      encoded |= ((unsigned int) operands->target & 0xff) << 6;
      break;

    case OASIS16_OPERANDS_RB:
      if (!oasis16_unsigned_range(operands->rb, 6))
        return false;
      encoded |= operands->rb << 14;
      break;

    case OASIS16_OPERANDS_RA_SPACE_ADDR11:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->address, 11)
          || !oasis16_unsigned_range(operands->mmio, 1))
        return false;
      encoded |= (operands->ra << 22) | (operands->mmio << OASIS16_MVF_MVT_MMIO_SHIFT)
                 | (operands->address << OASIS16_ADDR11_SHIFT);
      break;

    case OASIS16_OPERANDS_SPACE_ADDR11_IMM16:
      if (!oasis16_unsigned_range(operands->address, 11)
          || !oasis16_unsigned_range(operands->mmio, 1)
          || !oasis16_unsigned_range((unsigned int) operands->immediate, 16))
        return false;
      encoded |= (operands->mmio << OASIS16_MSI_MMIO_SHIFT)
                 | (operands->address << OASIS16_MSI_ADDR11_SHIFT)
                 | ((unsigned int) operands->immediate & 0xffff);
      break;

    case OASIS16_OPERANDS_RA_MEM_RB_OFF6:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->rb, 6)
          || !oasis16_signed_range(operands->offset, 6))
        return false;
      encoded |= (operands->ra << 20) | (operands->rb << 14)
                 | (((unsigned int) operands->offset & 0x3f) << 8);
      break;

    case OASIS16_OPERANDS_RB_SCRATCH11:
      if (!oasis16_unsigned_range(operands->rb, 6)
          || !oasis16_unsigned_range(operands->address, 11))
        return false;
      encoded |= (operands->rb << OASIS16_RA_TOOL_SHIFT)
                 | (operands->address << OASIS16_MCP_SCRATCH11_SHIFT);
      break;

    case OASIS16_OPERANDS_TRAP_IMM8:
      if (!oasis16_unsigned_range((unsigned int) operands->immediate, 8))
        return false;
      encoded |= (unsigned int) operands->immediate << OASIS16_SYSTEM_ARG8_SHIFT;
      break;

    case OASIS16_OPERANDS_RA_CSR8:
      if (!oasis16_unsigned_range(operands->ra, 6)
          || !oasis16_unsigned_range(operands->csr, 8))
        return false;
      encoded |= (operands->ra << OASIS16_SYSTEM_RA_SHIFT)
                 | (operands->csr << OASIS16_SYSTEM_ARG8_SHIFT);
      break;
    }

  *word = encoded;
  return true;
}

bool
oasis16_decode_instruction(unsigned int word,
                           const struct oasis16_opcode **opcode,
                           struct oasis16_insn *operands)
{
  unsigned int insn_class = (word >> OASIS16_CLASS_SHIFT) & OASIS16_CLASS_MASK;
  unsigned int opcode_bits;
  unsigned int i;

  if (insn_class == OASIS16_CLASS_REG || insn_class == OASIS16_CLASS_MEM)
    opcode_bits = (word >> OASIS16_REG_OPCODE_SHIFT) & OASIS16_OPCODE2_MASK;
  else
    opcode_bits = (word >> OASIS16_ALU_OPCODE_SHIFT) & OASIS16_OPCODE4_MASK;

  for (i = 0; i < oasis16_num_opcodes; i++)
    if (oasis16_opcodes[i].insn_class == insn_class
        && oasis16_opcodes[i].opcode == opcode_bits
        && (opcode_bits != 0xe || insn_class != OASIS16_CLASS_TOOL
            || oasis16_opcodes[i].subopcode
               == ((word >> OASIS16_SYSTEM_SUBOP_SHIFT)
                   & OASIS16_SYSTEM_SUBOP_MASK)))
      {
        const struct oasis16_opcode *op = &oasis16_opcodes[i];

        memset(operands, 0, sizeof(*operands));
        *opcode = op;

        switch (op->operands)
          {
          case OASIS16_OPERANDS_NONE:
            break;

          case OASIS16_OPERANDS_RA:
            operands->ra = (word >> OASIS16_RA_ALU_SHIFT) & OASIS16_REG_MASK;
            break;

          case OASIS16_OPERANDS_RA_RB:
            if (op->insn_class == OASIS16_CLASS_REG)
              {
                operands->ra = (word >> OASIS16_RA_REG_SHIFT) & OASIS16_REG_MASK;
                operands->rb = (word >> OASIS16_RB_REG_SHIFT) & OASIS16_REG_MASK;
              }
            else
              {
                operands->ra = (word >> OASIS16_RA_ALU_SHIFT) & OASIS16_REG_MASK;
                operands->rb = (word >> OASIS16_RB_ALU_SHIFT) & OASIS16_REG_MASK;
              }
            break;

          case OASIS16_OPERANDS_RA_IMM6:
            operands->ra = (word >> OASIS16_RA_ALU_SHIFT) & OASIS16_REG_MASK;
            operands->immediate = (word >> OASIS16_RB_ALU_SHIFT) & OASIS16_IMM6_MASK;
            break;

          case OASIS16_OPERANDS_RA_IMM16:
            if (op->insn_class == OASIS16_CLASS_REG)
              operands->ra = (word >> OASIS16_RA_REG_SHIFT) & OASIS16_REG_MASK;
            else
              operands->ra = (word >> OASIS16_RA_TOOL_SHIFT) & OASIS16_REG_MASK;
            operands->immediate = word & OASIS16_IMM16_MASK;
            break;

          case OASIS16_OPERANDS_RA_RB_TARGET8:
            operands->ra = (word >> OASIS16_RA_ALU_SHIFT) & OASIS16_REG_MASK;
            operands->rb = (word >> OASIS16_RB_ALU_SHIFT) & OASIS16_REG_MASK;
            operands->target = (word >> OASIS16_TARGET8_SHIFT) & OASIS16_TARGET8_MASK;
            break;

          case OASIS16_OPERANDS_TARGET8:
            operands->target = (word >> OASIS16_TARGET8_SHIFT) & OASIS16_TARGET8_MASK;
            break;

          case OASIS16_OPERANDS_RB:
            operands->rb = (word >> OASIS16_RB_TOOL_SHIFT) & OASIS16_REG_MASK;
            break;

          case OASIS16_OPERANDS_RA_SPACE_ADDR11:
            operands->ra = (word >> OASIS16_RA_MEM_SHIFT) & OASIS16_REG_MASK;
            operands->mmio = (word >> OASIS16_MVF_MVT_MMIO_SHIFT) & 1u;
            operands->address = (word >> OASIS16_ADDR11_SHIFT) & OASIS16_ADDR11_MASK;
            break;

          case OASIS16_OPERANDS_SPACE_ADDR11_IMM16:
            operands->mmio = (word >> OASIS16_MSI_MMIO_SHIFT) & 1u;
            operands->address = (word >> OASIS16_MSI_ADDR11_SHIFT) & OASIS16_ADDR11_MASK;
            operands->immediate = word & OASIS16_IMM16_MASK;
            break;

          case OASIS16_OPERANDS_RA_MEM_RB_OFF6:
            operands->ra = (word >> OASIS16_RA_TOOL_SHIFT) & OASIS16_REG_MASK;
            operands->rb = (word >> OASIS16_RB_TOOL_SHIFT) & OASIS16_REG_MASK;
            operands->offset = oasis16_sign_extend((word >> OASIS16_OFF6_SHIFT)
                                                   & OASIS16_IMM6_MASK, 6);
            break;

          case OASIS16_OPERANDS_RB_SCRATCH11:
            operands->rb = (word >> OASIS16_RA_TOOL_SHIFT) & OASIS16_REG_MASK;
            operands->address = (word >> OASIS16_MCP_SCRATCH11_SHIFT)
                                & OASIS16_ADDR11_MASK;
            break;

          case OASIS16_OPERANDS_TRAP_IMM8:
            if ((word & 0x003f00ffu) != 0)
              continue;
            operands->immediate = (word >> OASIS16_SYSTEM_ARG8_SHIFT)
                                  & OASIS16_SYSTEM_ARG8_MASK;
            break;

          case OASIS16_OPERANDS_RA_CSR8:
            if ((word & 0xffu) != 0)
              continue;
            operands->ra = (word >> OASIS16_SYSTEM_RA_SHIFT) & OASIS16_REG_MASK;
            operands->csr = (word >> OASIS16_SYSTEM_ARG8_SHIFT)
                            & OASIS16_SYSTEM_ARG8_MASK;
            break;
          }

        if (op->operands == OASIS16_OPERANDS_NONE
            && op->insn_class == OASIS16_CLASS_TOOL && op->opcode == 0xe
            && (word & 0x003fffffu) != 0)
          continue;

        return true;
      }

  *opcode = NULL;
  memset(operands, 0, sizeof(*operands));
  return false;
}

void
oasis16_print_instruction(const struct oasis16_opcode *opcode,
                          const struct oasis16_insn *operands,
                          fprintf_ftype fprintf_func,
                          void *stream)
{
  fprintf_func(stream, "%s", opcode->name);

  switch (opcode->operands)
    {
    case OASIS16_OPERANDS_NONE:
      break;
    case OASIS16_OPERANDS_RA:
      fprintf_func(stream, " r%u", operands->ra);
      break;
    case OASIS16_OPERANDS_RA_RB:
      fprintf_func(stream, " r%u, r%u", operands->ra, operands->rb);
      break;
    case OASIS16_OPERANDS_RA_IMM6:
    case OASIS16_OPERANDS_RA_IMM16:
      fprintf_func(stream, " r%u, %d", operands->ra, operands->immediate);
      break;
    case OASIS16_OPERANDS_RA_RB_TARGET8:
      fprintf_func(stream, " r%u, r%u, 0x%02x",
                   operands->ra, operands->rb, operands->target & 0xff);
      break;
    case OASIS16_OPERANDS_TARGET8:
      fprintf_func(stream, " 0x%02x", operands->target & 0xff);
      break;
    case OASIS16_OPERANDS_RB:
      fprintf_func(stream, " r%u", operands->rb);
      break;
    case OASIS16_OPERANDS_RA_SPACE_ADDR11:
      fprintf_func(stream, " r%u, %s:[0x%03x]", operands->ra,
                   operands->mmio ? "io" : "mem", operands->address);
      break;
    case OASIS16_OPERANDS_SPACE_ADDR11_IMM16:
      fprintf_func(stream, " %s:[0x%03x], %d", operands->mmio ? "io" : "mem",
                   operands->address, operands->immediate);
      break;
    case OASIS16_OPERANDS_RB_SCRATCH11:
      fprintf_func(stream, " [r%u], mem:[0x%03x]", operands->rb, operands->address);
      break;
    case OASIS16_OPERANDS_RA_MEM_RB_OFF6:
      fprintf_func(stream, " r%u, [r%u %c %u]",
                   operands->ra, operands->rb,
                   operands->offset < 0 ? '-' : '+',
                   operands->offset < 0 ? -operands->offset : operands->offset);
      break;
    case OASIS16_OPERANDS_TRAP_IMM8:
      fprintf_func(stream, " 0x%02x", operands->immediate & 0xff);
      break;
    case OASIS16_OPERANDS_RA_CSR8:
      fprintf_func(stream, " r%u, 0x%02x", operands->ra, operands->csr);
      break;
    }
}

int
print_insn_oasis16(bfd_vma memaddr, struct disassemble_info *info)
{
  bfd_byte buffer[OASIS16_INSN_SIZE];
  const struct oasis16_opcode *opcode;
  struct oasis16_insn operands;
  unsigned int word;
  int status;

  status = info->read_memory_func(memaddr, buffer, OASIS16_INSN_SIZE, info);
  if (status != 0)
    {
      info->memory_error_func(status, memaddr, info);
      return -1;
    }

  word = bfd_getl32(buffer);
  if (!oasis16_decode_instruction(word, &opcode, &operands))
    info->fprintf_func(info->stream, ".word 0x%08x", word);
  else
    oasis16_print_instruction(opcode, &operands, info->fprintf_func, info->stream);

  return OASIS16_INSN_SIZE;
}
