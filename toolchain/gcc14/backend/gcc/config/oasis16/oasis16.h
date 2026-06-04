#ifndef GCC_OASIS16_H
#define GCC_OASIS16_H

#define TARGET_CPU_CPP_BUILTINS() \
  do { \
    builtin_define("__OASIS16__"); \
    builtin_define("__OASIS_BASE16T__"); \
  } while (0)

#define BITS_BIG_ENDIAN 0
#define BYTES_BIG_ENDIAN 0
#define WORDS_BIG_ENDIAN 0

#define UNITS_PER_WORD 2
#define BITS_PER_UNIT 8
#define INT_TYPE_SIZE 16
#define SHORT_TYPE_SIZE 16
#define LONG_TYPE_SIZE 32
#define LONG_LONG_TYPE_SIZE 64
#define POINTER_SIZE 16
#define PARM_BOUNDARY 16
#define STACK_BOUNDARY 16
#define FUNCTION_BOUNDARY 16
#define BIGGEST_ALIGNMENT 16
#define STRICT_ALIGNMENT 0

#define FIRST_PSEUDO_REGISTER 64

#define FIXED_REGISTERS \
  { \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1 \
  }

#define CALL_USED_REGISTERS \
  { \
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1 \
  }

#define REG_ALLOC_ORDER \
  { \
    12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, \
    24, 25, 26, 27, 28, 29, 30, 31, \
    4, 5, 6, 7, 8, 9, 10, 11, \
    1, 2, 3, \
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, \
    44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, \
    0, 56, 57, 58, 59, 60, 61, 62, 63 \
  }

#define HARD_REGNO_NREGS(REGNO, MODE) 1
#define HARD_REGNO_MODE_OK(REGNO, MODE) 1
#define MODES_TIEABLE_P(MODE1, MODE2) 1

enum reg_class {
  NO_REGS,
  GENERAL_REGS,
  ALL_REGS,
  LIM_REG_CLASSES
};

#define N_REG_CLASSES ((int) LIM_REG_CLASSES)
#define REG_CLASS_NAMES { "NO_REGS", "GENERAL_REGS", "ALL_REGS" }
#define REG_CLASS_CONTENTS \
  { \
    { 0, 0 }, \
    { 0xffffffff, 0x00ffffff }, \
    { 0xffffffff, 0xffffffff } \
  }

#define GENERAL_REGS GENERAL_REGS
#define BASE_REG_CLASS GENERAL_REGS
#define INDEX_REG_CLASS NO_REGS
#define REGNO_REG_CLASS(REGNO) GENERAL_REGS
#define CLASS_MAX_NREGS(CLASS, MODE) 1

#define STACK_POINTER_REGNUM 56
#define FRAME_POINTER_REGNUM 57
#define RETURN_ADDRESS_REGNUM 58
#define HARD_FRAME_POINTER_REGNUM FRAME_POINTER_REGNUM
#define ARG_POINTER_REGNUM FRAME_POINTER_REGNUM
#define STATIC_CHAIN_REGNUM 55

#define FIRST_PARM_REGNUM 4
#define FUNCTION_VALUE_REGNO_P(N) ((N) == 1 || (N) == 2)
#define FUNCTION_ARG_REGNO_P(N) ((N) >= 4 && (N) <= 11)

#define Pmode HImode
#define STACK_GROWS_DOWNWARD 1
#define FRAME_GROWS_DOWNWARD 1
#define STARTING_FRAME_OFFSET 0

#define ELIMINABLE_REGS \
  { { ARG_POINTER_REGNUM, STACK_POINTER_REGNUM }, \
    { ARG_POINTER_REGNUM, FRAME_POINTER_REGNUM }, \
    { FRAME_POINTER_REGNUM, STACK_POINTER_REGNUM } }

#define INITIAL_ELIMINATION_OFFSET(FROM, TO, OFFSET) ((OFFSET) = 0)

#define REGISTER_NAMES \
  { \
    "r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", \
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15", \
    "r16", "r17", "r18", "r19", "r20", "r21", "r22", "r23", \
    "r24", "r25", "r26", "r27", "r28", "r29", "r30", "r31", \
    "r32", "r33", "r34", "r35", "r36", "r37", "r38", "r39", \
    "r40", "r41", "r42", "r43", "r44", "r45", "r46", "r47", \
    "r48", "r49", "r50", "r51", "r52", "r53", "r54", "r55", \
    "r56", "r57", "r58", "r59", "r60", "r61", "r62", "r63" \
  }

#define PRINT_OPERAND(STREAM, X, CODE) oasis16_print_operand(STREAM, X, CODE)
#define PRINT_OPERAND_ADDRESS(STREAM, X) oasis16_print_operand_address(STREAM, X)

#define ASM_APP_ON ";APP\n"
#define ASM_APP_OFF ";NO_APP\n"
#define ASM_COMMENT_START ";"

#define HAS_INIT_SECTION 1
#define TRAMPOLINE_SIZE 0

#endif
