#ifndef GCC_OASIS16_PROTOS_H
#define GCC_OASIS16_PROTOS_H

extern void oasis16_expand_prologue(void);
extern void oasis16_expand_epilogue(void);
extern int oasis16_initial_elimination_offset(int from, int to);
extern void oasis16_print_operand(FILE *file, rtx x, int code);
extern void oasis16_print_operand_address(FILE *file, rtx x);
extern bool oasis16_legitimate_address_p(machine_mode mode, rtx x, bool strict);
extern rtx oasis16_return_addr_rtx(int count, rtx frame);

#endif
