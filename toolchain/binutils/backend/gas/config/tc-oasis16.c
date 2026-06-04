#include "as.h"
#include "safe-ctype.h"
#include "subsegs.h"
#include "opcode/oasis16.h"

const char comment_chars[] = ";";
const char line_comment_chars[] = ";";
const char line_separator_chars[] = "";
const char EXP_CHARS[] = "eE";
const char FLT_CHARS[] = "rRsSfFdDxXpP";

void
md_begin(void)
{
}

void
md_assemble(char *str)
{
  as_bad(_("OASIS16 GAS encoder is not implemented yet: %s"), str);
}

const char *
md_atof(int type, char *litP, int *sizeP)
{
  return ieee_md_atof(type, litP, sizeP, FALSE);
}

void
md_apply_fix(fixS *fixP ATTRIBUTE_UNUSED,
             valueT *valP ATTRIBUTE_UNUSED,
             segT seg ATTRIBUTE_UNUSED)
{
}

arelent *
tc_gen_reloc(asection *section ATTRIBUTE_UNUSED, fixS *fixP ATTRIBUTE_UNUSED)
{
  return NULL;
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
