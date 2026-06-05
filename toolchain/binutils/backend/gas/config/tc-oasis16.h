#ifndef TC_OASIS16_H
#define TC_OASIS16_H

#define TC_OASIS16 1
#define TARGET_FORMAT "elf32-oasis16"
#define TARGET_ARCH bfd_arch_oasis16
#define TARGET_BYTES_BIG_ENDIAN 0
#define WORKING_DOT_WORD 1
#define LISTING_HEADER "OASIS Base-16T GAS"

#define md_number_to_chars number_to_chars_littleendian
#define md_estimate_size_before_relax(f, s) \
  (as_fatal (_("OASIS relaxation is not implemented")), 0)
#define md_convert_frag(b, s, f) \
  as_fatal (_("OASIS relaxation is not implemented"))

#define tc_canonicalize_symbol_name(str) (str)
#define tc_unrecognized_line(ch) 0
#define md_operand(x)

#endif
