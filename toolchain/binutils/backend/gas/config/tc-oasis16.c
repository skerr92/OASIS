#include "as.h"
#include "safe-ctype.h"
#include "subsegs.h"
#include "opcode/oasis16.h"
#include "elf/oasis16.h"

const char comment_chars[] = ";#";
const char line_comment_chars[] = ";#";
const char line_separator_chars[] = "";
const char EXP_CHARS[] = "eE";
const char FLT_CHARS[] = "rRsSfFdDxXpP";

const char md_shortopts[] = "";

const struct option md_longopts[] =
{
  { NULL, no_argument, NULL, 0 }
};

const size_t md_longopts_size = sizeof(md_longopts);

const pseudo_typeS md_pseudo_table[] =
{
  { NULL, NULL, 0 }
};

int
md_parse_option(int c ATTRIBUTE_UNUSED, const char *arg ATTRIBUTE_UNUSED)
{
  return 0;
}

void
md_show_usage(FILE *stream ATTRIBUTE_UNUSED)
{
}

symbolS *
md_undefined_symbol(char *name ATTRIBUTE_UNUSED)
{
  return NULL;
}

static char *
skip_space(char *input)
{
  while (ISSPACE(*input))
    input++;
  return input;
}

static char *
skip_comma(char *input)
{
  input = skip_space(input);
  if (*input != ',')
    {
      as_bad(_("expected comma"));
      return input;
    }
  return skip_space(input + 1);
}

static char *
parse_register(char *input, unsigned int *regno)
{
  char *start;
  long value;

  input = skip_space(input);
  if (*input != 'r' && *input != 'R')
    {
      as_bad(_("expected register"));
      return input;
    }

  input++;
  start = input;
  value = strtol(input, &input, 10);
  if (input == start || value < 0 || value > 63)
    as_bad(_("register out of range"));
  *regno = (unsigned int) value;
  return skip_space(input);
}

static char *
parse_absolute(char *input, expressionS *expression_p)
{
  char *saved_input_line_pointer = input_line_pointer;

  input = skip_space(input);
  input_line_pointer = input;
  expression(expression_p);
  input = input_line_pointer;
  input_line_pointer = saved_input_line_pointer;
  return skip_space(input);
}

static int
expression_is_constant(expressionS *expression_p, int *value)
{
  if (expression_p->X_op != O_constant)
    return 0;

  *value = (int) expression_p->X_add_number;
  return 1;
}

static char *
parse_addr12(char *input, expressionS *expression_p)
{
  input = skip_space(input);
  if (*input != '[')
    {
      as_bad(_("expected '['"));
      return input;
    }
  input = parse_absolute(input + 1, expression_p);
  if (*input != ']')
    as_bad(_("expected ']'"));
  else
    input++;
  return skip_space(input);
}

static char *
parse_reg_offset_mem(char *input, unsigned int *rb, int *offset)
{
  input = skip_space(input);
  if (*input != '[')
    {
      as_bad(_("expected '['"));
      return input;
    }

  input = parse_register(input + 1, rb);
  *offset = 0;

  if (*input == '+' || *input == '-')
    {
      int sign = *input == '-' ? -1 : 1;
      expressionS expr;
      int value;

      input = parse_absolute(input + 1, &expr);
      if (!expression_is_constant(&expr, &value))
        as_bad(_("register-relative offset must be absolute"));
      *offset = sign * value;
    }

  if (*input != ']')
    as_bad(_("expected ']'"));
  else
    input++;

  return skip_space(input);
}

static bfd_reloc_code_real_type
reloc_for_operand(const struct oasis16_opcode *opcode)
{
  switch (opcode->operands)
    {
    case OASIS16_OPERANDS_RA_IMM16:
      return BFD_RELOC_OASIS16_16;
    case OASIS16_OPERANDS_ADDR12_IMM16:
      return BFD_RELOC_OASIS16_MSI_ADDR12;
    case OASIS16_OPERANDS_TARGET8:
    case OASIS16_OPERANDS_RA_RB_TARGET8:
      return BFD_RELOC_OASIS16_CALL8;
    case OASIS16_OPERANDS_RA_ADDR12:
      return BFD_RELOC_OASIS16_ADDR12;
    default:
      return BFD_RELOC_NONE;
    }
}

static void
emit_instruction(unsigned int word, expressionS *reloc_expr,
                 bfd_reloc_code_real_type reloc)
{
  char *frag = frag_more(4);

  md_number_to_chars(frag, word, 4);

  if (reloc_expr != NULL && reloc != BFD_RELOC_NONE && reloc_expr->X_op != O_constant)
    fix_new_exp(frag_now, frag - frag_now->fr_literal, 4, reloc_expr, 0, reloc);
}

void
md_begin(void)
{
}

void
md_assemble(char *str)
{
  char *input = str;
  char mnemonic[16];
  char *out = mnemonic;
  const struct oasis16_opcode *opcode;
  struct oasis16_insn operands;
  expressionS reloc_expr;
  expressionS tmp_expr;
  expressionS *reloc_ptr = NULL;
  bfd_reloc_code_real_type reloc = BFD_RELOC_NONE;
  unsigned int word;
  int value;

  memset(&operands, 0, sizeof(operands));
  memset(&reloc_expr, 0, sizeof(reloc_expr));

  input = skip_space(input);
  while (*input && !ISSPACE(*input) && *input != ',' && (out - mnemonic) < 15)
    *out++ = TOUPPER(*input++);
  *out = 0;

  opcode = oasis16_lookup_opcode(mnemonic);
  if (opcode == NULL)
    {
      as_bad(_("unknown OASIS instruction: %s"), mnemonic);
      return;
    }

  input = skip_space(input);

  switch (opcode->operands)
    {
    case OASIS16_OPERANDS_NONE:
      break;

    case OASIS16_OPERANDS_RA:
      input = parse_register(input, &operands.ra);
      break;

    case OASIS16_OPERANDS_RA_RB:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_register(input, &operands.rb);
      break;

    case OASIS16_OPERANDS_RA_IMM6:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_absolute(input, &tmp_expr);
      if (!expression_is_constant(&tmp_expr, &value))
        as_bad(_("imm6 must be absolute"));
      operands.immediate = value;
      break;

    case OASIS16_OPERANDS_RA_IMM16:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_absolute(input, &reloc_expr);
      if (expression_is_constant(&reloc_expr, &value))
        operands.immediate = value;
      else
        reloc_ptr = &reloc_expr;
      break;

    case OASIS16_OPERANDS_RA_RB_TARGET8:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_register(input, &operands.rb);
      input = skip_comma(input);
      input = parse_absolute(input, &reloc_expr);
      if (expression_is_constant(&reloc_expr, &value))
        operands.target = value;
      else
        reloc_ptr = &reloc_expr;
      break;

    case OASIS16_OPERANDS_TARGET8:
      input = parse_absolute(input, &reloc_expr);
      if (expression_is_constant(&reloc_expr, &value))
        operands.target = value;
      else
        reloc_ptr = &reloc_expr;
      break;

    case OASIS16_OPERANDS_RB:
      input = parse_register(input, &operands.rb);
      break;

    case OASIS16_OPERANDS_RA_ADDR12:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_addr12(input, &reloc_expr);
      if (expression_is_constant(&reloc_expr, &value))
        operands.address = (unsigned int) value;
      else
        reloc_ptr = &reloc_expr;
      break;

    case OASIS16_OPERANDS_ADDR12_IMM16:
      input = parse_addr12(input, &reloc_expr);
      if (expression_is_constant(&reloc_expr, &value))
        operands.address = (unsigned int) value;
      else
        reloc_ptr = &reloc_expr;
      input = skip_comma(input);
      input = parse_absolute(input, &tmp_expr);
      if (!expression_is_constant(&tmp_expr, &value))
        as_bad(_("MSI immediate must be absolute"));
      operands.immediate = value;
      break;

    case OASIS16_OPERANDS_RA_MEM_RB_OFF6:
      input = parse_register(input, &operands.ra);
      input = skip_comma(input);
      input = parse_reg_offset_mem(input, &operands.rb, &operands.offset);
      break;
    }

  input = skip_space(input);
  if (*input != 0)
    as_bad(_("junk at end of instruction: %s"), input);

  reloc = reloc_for_operand(opcode);
  if (!oasis16_encode_instruction(opcode, &operands, &word))
    {
      as_bad(_("operand out of range for %s"), opcode->name);
      return;
    }

  emit_instruction(word, reloc_ptr, reloc);
}

const char *
md_atof(int type, char *litP, int *sizeP)
{
  return ieee_md_atof(type, litP, sizeP, false);
}

void
md_apply_fix(fixS *fixP, valueT *valP, segT seg ATTRIBUTE_UNUSED)
{
  unsigned char *where = (unsigned char *) fixP->fx_frag->fr_literal + fixP->fx_where;
  unsigned int instruction = bfd_get_32(stdoutput, where);
  valueT value = *valP;

  switch (fixP->fx_r_type)
    {
    case BFD_RELOC_OASIS16_16:
      instruction |= value & 0xffff;
      break;
    case BFD_RELOC_OASIS16_ADDR12:
      instruction |= (value & 0xfff) << 10;
      break;
    case BFD_RELOC_OASIS16_MSI_ADDR12:
      instruction |= (value & 0xfff) << 16;
      break;
    case BFD_RELOC_OASIS16_CALL8:
      instruction |= (value & 0xff) << 6;
      break;
    default:
      break;
    }

  bfd_put_32(stdoutput, instruction, where);
  fixP->fx_done = 1;
}

arelent *
tc_gen_reloc(asection *section ATTRIBUTE_UNUSED, fixS *fixP)
{
  arelent *reloc = XNEW(arelent);

  reloc->sym_ptr_ptr = XNEW(asymbol *);
  *reloc->sym_ptr_ptr = symbol_get_bfdsym(fixP->fx_addsy);
  reloc->address = fixP->fx_frag->fr_address + fixP->fx_where;
  reloc->addend = fixP->fx_offset;
  reloc->howto = bfd_reloc_type_lookup(stdoutput, fixP->fx_r_type);

  if (reloc->howto == NULL)
    as_bad_where(fixP->fx_file, fixP->fx_line, _("cannot represent relocation"));

  return reloc;
}

valueT
md_section_align(segT segment ATTRIBUTE_UNUSED, valueT size)
{
  return size;
}

long
md_pcrel_from(fixS *fixP ATTRIBUTE_UNUSED)
{
  return 0;
}
