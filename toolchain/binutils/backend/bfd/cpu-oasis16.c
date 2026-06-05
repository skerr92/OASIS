#include "sysdep.h"
#include "bfd.h"
#include "libbfd.h"

const bfd_arch_info_type bfd_oasis16_arch =
{
  16,
  16,
  8,
  bfd_arch_oasis16,
  0,
  "oasis16",
  "oasis16",
  1,
  true,
  bfd_default_compatible,
  bfd_default_scan,
  bfd_arch_default_fill,
  NULL,
  0
};
