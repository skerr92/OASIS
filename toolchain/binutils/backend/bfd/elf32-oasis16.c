#include "sysdep.h"
#include "bfd.h"
#include "libbfd.h"
#include "elf-bfd.h"
#include "elf/oasis16.h"

static reloc_howto_type oasis16_elf_howto_table[] =
{
  HOWTO(R_OASIS16_NONE, 0, 0, 0, FALSE, 0, complain_overflow_dont,
        bfd_elf_generic_reloc, "R_OASIS16_NONE", FALSE, 0, 0, FALSE),

  HOWTO(R_OASIS16_16, 0, 1, 16, FALSE, 0, complain_overflow_unsigned,
        bfd_elf_generic_reloc, "R_OASIS16_16", FALSE, 0, 0xffff, FALSE),

  HOWTO(R_OASIS16_ADDR9, 13, 2, 9, FALSE, 0, complain_overflow_unsigned,
        bfd_elf_generic_reloc, "R_OASIS16_ADDR9", FALSE, 0, 0x003fe000, FALSE),

  HOWTO(R_OASIS16_TARGET8, 6, 2, 8, FALSE, 0, complain_overflow_unsigned,
        bfd_elf_generic_reloc, "R_OASIS16_TARGET8", FALSE, 0, 0x00003fc0, FALSE),

  HOWTO(R_OASIS16_CALL8, 6, 2, 8, FALSE, 0, complain_overflow_unsigned,
        bfd_elf_generic_reloc, "R_OASIS16_CALL8", FALSE, 0, 0x00003fc0, FALSE),
};

static reloc_howto_type *
oasis16_reloc_type_lookup(bfd *abfd ATTRIBUTE_UNUSED, bfd_reloc_code_real_type code)
{
  switch (code)
    {
    case BFD_RELOC_NONE:
      return &oasis16_elf_howto_table[R_OASIS16_NONE];
    case BFD_RELOC_16:
    case BFD_RELOC_OASIS16_16:
      return &oasis16_elf_howto_table[R_OASIS16_16];
    case BFD_RELOC_OASIS16_ADDR9:
      return &oasis16_elf_howto_table[R_OASIS16_ADDR9];
    case BFD_RELOC_OASIS16_TARGET8:
      return &oasis16_elf_howto_table[R_OASIS16_TARGET8];
    case BFD_RELOC_OASIS16_CALL8:
      return &oasis16_elf_howto_table[R_OASIS16_CALL8];
    default:
      return NULL;
    }
}

static reloc_howto_type *
oasis16_reloc_name_lookup(bfd *abfd ATTRIBUTE_UNUSED, const char *r_name)
{
  unsigned int i;

  for (i = 0; i < ARRAY_SIZE(oasis16_elf_howto_table); i++)
    if (oasis16_elf_howto_table[i].name != NULL
        && strcasecmp(oasis16_elf_howto_table[i].name, r_name) == 0)
      return &oasis16_elf_howto_table[i];

  return NULL;
}

static void
oasis16_info_to_howto_rela(bfd *abfd ATTRIBUTE_UNUSED,
                           arelent *cache_ptr,
                           Elf_Internal_Rela *dst)
{
  unsigned int r_type = ELF32_R_TYPE(dst->r_info);

  if (r_type < ARRAY_SIZE(oasis16_elf_howto_table))
    cache_ptr->howto = &oasis16_elf_howto_table[r_type];
}

#define ELF_ARCH bfd_arch_oasis16
#define ELF_TARGET_ID OASIS16_ELF_DATA
#define ELF_MACHINE_CODE EM_OASIS16
#define ELF_MAXPAGESIZE 1
#define TARGET_LITTLE_SYM oasis16_elf32_vec
#define TARGET_LITTLE_NAME "elf32-oasis16"
#define elf_info_to_howto_rel NULL
#define elf_info_to_howto oasis16_info_to_howto_rela
#define elf_backend_rela_normal 1
#define bfd_elf32_bfd_reloc_type_lookup oasis16_reloc_type_lookup
#define bfd_elf32_bfd_reloc_name_lookup oasis16_reloc_name_lookup

#include "elf32-target.h"
