#define IN_TARGET_CODE 1

#include "config.h"
#include "system.h"
#include "coretypes.h"
#include "backend.h"
#include "target.h"
#include "rtl.h"
#include "tree.h"
#include "stringpool.h"
#include "attribs.h"
#include "df.h"
#include "memmodel.h"
#include "tm_p.h"
#include "regs.h"
#include "emit-rtl.h"
#include "output.h"
#include "insn-config.h"
#include "insn-attr.h"
#include "recog.h"
#include "calls.h"
#include "explow.h"
#include "expr.h"
#include "function.h"
#include "builtins.h"

/* This file should be included last.  */
#include "target-def.h"

static void
oasis16_option_override(void)
{
}

static bool oasis16_save_reg_p(unsigned int regno);
static unsigned int oasis16_saved_reg_count(void);

static unsigned int
oasis16_hard_regno_nregs(unsigned int regno ATTRIBUTE_UNUSED, machine_mode mode)
{
  return (GET_MODE_SIZE(mode) + UNITS_PER_WORD - 1) / UNITS_PER_WORD;
}

static bool
oasis16_hard_regno_mode_ok(unsigned int regno ATTRIBUTE_UNUSED,
                           machine_mode mode ATTRIBUTE_UNUSED)
{
  return true;
}

static bool
oasis16_modes_tieable_p(machine_mode mode1 ATTRIBUTE_UNUSED,
                        machine_mode mode2 ATTRIBUTE_UNUSED)
{
  return true;
}

static HOST_WIDE_INT
oasis16_starting_frame_offset(void)
{
  return 0;
}

static unsigned int
oasis16_arg_words(machine_mode mode, const_tree type)
{
  HOST_WIDE_INT size;

  if (mode == BLKmode && type != NULL_TREE)
    size = int_size_in_bytes(type);
  else
    size = GET_MODE_SIZE(mode);

  if (size <= 0)
    size = UNITS_PER_WORD;

  return (size + UNITS_PER_WORD - 1) / UNITS_PER_WORD;
}

static rtx
oasis16_function_arg(cumulative_args_t cum_v, const function_arg_info &arg)
{
  CUMULATIVE_ARGS *cum = get_cumulative_args(cum_v);
  unsigned int words = oasis16_arg_words(arg.mode, arg.type);

  if (*cum + words <= (OASIS16_LAST_ARG_REGNUM - OASIS16_FIRST_ARG_REGNUM + 1))
    return gen_rtx_REG(arg.mode, OASIS16_FIRST_ARG_REGNUM + *cum);

  return NULL_RTX;
}

static void
oasis16_function_arg_advance(cumulative_args_t cum_v, const function_arg_info &arg)
{
  CUMULATIVE_ARGS *cum = get_cumulative_args(cum_v);
  *cum += oasis16_arg_words(arg.mode, arg.type);
}

static rtx
oasis16_function_value(const_tree valtype, const_tree fn_decl_or_type ATTRIBUTE_UNUSED,
                       bool outgoing ATTRIBUTE_UNUSED)
{
  return gen_rtx_REG(TYPE_MODE(valtype), OASIS16_RETVAL_REGNUM);
}

static rtx
oasis16_libcall_value(machine_mode mode, const_rtx fun ATTRIBUTE_UNUSED)
{
  return gen_rtx_REG(mode, OASIS16_RETVAL_REGNUM);
}

static bool
oasis16_function_value_regno_p(const unsigned int regno)
{
  return regno == OASIS16_RETVAL_REGNUM || regno == OASIS16_RETVAL_REGNUM + 1;
}

static bool
oasis16_return_in_memory(const_tree type, const_tree fntype ATTRIBUTE_UNUSED)
{
  return int_size_in_bytes(type) > 2 * UNITS_PER_WORD;
}

int
oasis16_initial_elimination_offset(int from, int to)
{
  HOST_WIDE_INT frame_size =
    get_frame_size().to_constant() + oasis16_saved_reg_count() * UNITS_PER_WORD;

  if (from == ARG_POINTER_REGNUM && to == STACK_POINTER_REGNUM)
    return frame_size;
  if (from == ARG_POINTER_REGNUM && to == FRAME_POINTER_REGNUM)
    return 0;
  if (from == FRAME_POINTER_REGNUM && to == STACK_POINTER_REGNUM)
    return frame_size;

  return 0;
}

static bool
oasis16_offset_address_p(rtx x, bool strict)
{
  rtx base;
  rtx offset;

  if (REG_P(x))
    return !strict || REGNO_OK_FOR_BASE_P(REGNO(x));

  if (GET_CODE(x) != PLUS)
    return false;

  base = XEXP(x, 0);
  offset = XEXP(x, 1);

  if (!REG_P(base) || !CONST_INT_P(offset))
    return false;

  if (strict && !REGNO_OK_FOR_BASE_P(REGNO(base)))
    return false;

  return IN_RANGE(INTVAL(offset), -32, 31);
}

bool
oasis16_legitimate_address_p(machine_mode mode ATTRIBUTE_UNUSED, rtx x, bool strict,
                             code_helper)
{
  return oasis16_offset_address_p(x, strict);
}

static bool
oasis16_lra_p(void)
{
  return true;
}

static bool
oasis16_save_reg_p(unsigned int regno)
{
  if (regno == RETURN_ADDRESS_REGNUM)
    return !crtl->is_leaf;

  return regno < FIRST_PSEUDO_REGISTER
         && !fixed_regs[regno]
         && !call_used_regs[regno]
         && df_regs_ever_live_p(regno);
}

static unsigned int
oasis16_saved_reg_count(void)
{
  unsigned int count = 0;

  for (unsigned int regno = 0; regno < FIRST_PSEUDO_REGISTER; regno++)
    if (oasis16_save_reg_p(regno))
      count++;

  return count;
}

rtx
oasis16_return_addr_rtx(int count, rtx frame ATTRIBUTE_UNUSED)
{
  if (count != 0)
    return NULL_RTX;

  return gen_rtx_REG(Pmode, RETURN_ADDRESS_REGNUM);
}

static void
oasis16_adjust_stack(HOST_WIDE_INT amount)
{
  rtx sp = gen_rtx_REG(HImode, STACK_POINTER_REGNUM);

  if (amount == 0)
    return;

  if (amount > 0)
    emit_insn(gen_subhi3(sp, sp, GEN_INT(amount)));
  else
    emit_insn(gen_addhi3(sp, sp, GEN_INT(-amount)));
}

static rtx_insn *
oasis16_emit_recognized(rtx pattern)
{
  rtx_insn *insn = emit_insn(pattern);
  recog_memoized(insn);
  return insn;
}

static rtx_insn *
oasis16_emit_recognized_jump(rtx pattern)
{
  rtx_insn *insn = emit_jump_insn(pattern);
  recog_memoized(insn);
  return insn;
}

static rtx
oasis16_stack_slot(unsigned int word_offset)
{
  rtx sp = gen_rtx_REG(HImode, STACK_POINTER_REGNUM);

  gcc_assert(word_offset <= 31);

  if (word_offset == 0)
    return gen_rtx_MEM(HImode, sp);

  return gen_rtx_MEM(HImode, gen_rtx_PLUS(HImode, sp, GEN_INT(word_offset)));
}

void
oasis16_expand_prologue(void)
{
  HOST_WIDE_INT frame_size = get_frame_size().to_constant();
  unsigned int slot = 0;

  oasis16_adjust_stack(frame_size + oasis16_saved_reg_count() * UNITS_PER_WORD);

  for (unsigned int regno = 0; regno < FIRST_PSEUDO_REGISTER; regno++)
    if (oasis16_save_reg_p(regno))
      oasis16_emit_recognized(gen_movhi(oasis16_stack_slot(slot++),
                                        gen_rtx_REG(HImode, regno)));

  if (frame_pointer_needed)
    oasis16_emit_recognized(gen_movhi(gen_rtx_REG(HImode, FRAME_POINTER_REGNUM),
                                      gen_rtx_REG(HImode, STACK_POINTER_REGNUM)));
}

void
oasis16_expand_epilogue(void)
{
  HOST_WIDE_INT frame_size = get_frame_size().to_constant();
  unsigned int slot = 0;

  if (frame_pointer_needed)
    oasis16_emit_recognized(gen_movhi(gen_rtx_REG(HImode, STACK_POINTER_REGNUM),
                                      gen_rtx_REG(HImode, FRAME_POINTER_REGNUM)));

  for (unsigned int regno = 0; regno < FIRST_PSEUDO_REGISTER; regno++)
    if (oasis16_save_reg_p(regno))
      oasis16_emit_recognized(gen_movhi(gen_rtx_REG(HImode, regno),
                                        oasis16_stack_slot(slot++)));

  oasis16_adjust_stack(-(frame_size + oasis16_saved_reg_count() * UNITS_PER_WORD));
  oasis16_emit_recognized_jump(gen_returner());
}

void
oasis16_print_operand(FILE *file, rtx x, int code ATTRIBUTE_UNUSED)
{
  switch (GET_CODE(x))
    {
    case REG:
      fprintf(file, "r%d", REGNO(x));
      break;
    case MEM:
      oasis16_print_operand_address(file, XEXP(x, 0));
      break;
    case CONST_INT:
      fprintf(file, HOST_WIDE_INT_PRINT_DEC, INTVAL(x));
      break;
    case SYMBOL_REF:
    case LABEL_REF:
      output_addr_const(file, x);
      break;
    default:
      output_addr_const(file, x);
      break;
    }
}

void
oasis16_print_operand_address(FILE *file, rtx x)
{
  if (REG_P(x))
    {
      fprintf(file, "[r%d + 0]", REGNO(x));
      return;
    }

  if (GET_CODE(x) == PLUS && REG_P(XEXP(x, 0)) && CONST_INT_P(XEXP(x, 1)))
    {
      fprintf(file, "[r%d %c " HOST_WIDE_INT_PRINT_DEC "]",
              REGNO(XEXP(x, 0)),
              INTVAL(XEXP(x, 1)) < 0 ? '-' : '+',
              llabs(INTVAL(XEXP(x, 1))));
      return;
    }

  output_addr_const(file, x);
}

static void
oasis16_globalize_label(FILE *file, const char *name)
{
  fputs("\t.global\t", file);
  assemble_name(file, name);
  fputc('\n', file);
}

#undef TARGET_OPTION_OVERRIDE
#define TARGET_OPTION_OVERRIDE oasis16_option_override

#undef TARGET_ASM_GLOBALIZE_LABEL
#define TARGET_ASM_GLOBALIZE_LABEL oasis16_globalize_label

#undef TARGET_FUNCTION_ARG
#define TARGET_FUNCTION_ARG oasis16_function_arg

#undef TARGET_HARD_REGNO_NREGS
#define TARGET_HARD_REGNO_NREGS oasis16_hard_regno_nregs

#undef TARGET_HARD_REGNO_MODE_OK
#define TARGET_HARD_REGNO_MODE_OK oasis16_hard_regno_mode_ok

#undef TARGET_MODES_TIEABLE_P
#define TARGET_MODES_TIEABLE_P oasis16_modes_tieable_p

#undef TARGET_STARTING_FRAME_OFFSET
#define TARGET_STARTING_FRAME_OFFSET oasis16_starting_frame_offset

#undef TARGET_FUNCTION_ARG_ADVANCE
#define TARGET_FUNCTION_ARG_ADVANCE oasis16_function_arg_advance

#undef TARGET_FUNCTION_VALUE
#define TARGET_FUNCTION_VALUE oasis16_function_value

#undef TARGET_LIBCALL_VALUE
#define TARGET_LIBCALL_VALUE oasis16_libcall_value

#undef TARGET_FUNCTION_VALUE_REGNO_P
#define TARGET_FUNCTION_VALUE_REGNO_P oasis16_function_value_regno_p

#undef TARGET_RETURN_IN_MEMORY
#define TARGET_RETURN_IN_MEMORY oasis16_return_in_memory

#undef TARGET_LRA_P
#define TARGET_LRA_P oasis16_lra_p

#undef TARGET_LEGITIMATE_ADDRESS_P
#define TARGET_LEGITIMATE_ADDRESS_P oasis16_legitimate_address_p

struct gcc_target targetm = TARGET_INITIALIZER;
