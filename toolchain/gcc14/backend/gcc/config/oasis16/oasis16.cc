#include "config.h"
#include "system.h"
#include "coretypes.h"
#include "backend.h"
#include "target.h"
#include "rtl.h"
#include "tree.h"
#include "memmodel.h"
#include "tm_p.h"
#include "target-def.h"
#include "output.h"
#include "insn-attr.h"

static void
oasis16_option_override(void)
{
}

void
oasis16_expand_prologue(void)
{
}

void
oasis16_expand_epilogue(void)
{
  emit_jump_insn(gen_returner());
}

void
oasis16_print_operand(FILE *file, rtx x, int code ATTRIBUTE_UNUSED)
{
  switch (GET_CODE(x))
    {
    case REG:
      fprintf(file, "r%d", REGNO(x));
      break;
    case CONST_INT:
      fprintf(file, HOST_WIDE_INT_PRINT_DEC, INTVAL(x));
      break;
    default:
      output_addr_const(file, x);
      break;
    }
}

void
oasis16_print_operand_address(FILE *file, rtx x)
{
  if (GET_CODE(x) == REG)
    {
      fprintf(file, "[r%d + 0]", REGNO(x));
      return;
    }

  if (GET_CODE(x) == PLUS && GET_CODE(XEXP(x, 0)) == REG && CONST_INT_P(XEXP(x, 1)))
    {
      fprintf(file, "[r%d + " HOST_WIDE_INT_PRINT_DEC "]",
              REGNO(XEXP(x, 0)), INTVAL(XEXP(x, 1)));
      return;
    }

  output_addr_const(file, x);
}

#undef TARGET_OPTION_OVERRIDE
#define TARGET_OPTION_OVERRIDE oasis16_option_override

struct gcc_target targetm = TARGET_INITIALIZER;
