OUTPUT_ARCH(oasis16)
ENTRY(_start)

MEMORY
{
  imem (rx)  : ORIGIN = 0x0000, LENGTH = 0x0400
  dmem (rw)  : ORIGIN = 0x0400, LENGTH = 0x0c00
}

SECTIONS
{
  .text 0x0000 :
  {
    KEEP(*(.text.startup))
    *(.text.start)
    *(.text .text.*)
  } > imem

  .rodata :
  {
    *(.rodata .rodata.*)
  } > dmem

  .init_array :
  {
    __oasis_init_array_start = .;
    KEEP(*(.init_array .init_array.*))
    __oasis_init_array_end = .;
  } > dmem

  .fini_array :
  {
    __oasis_fini_array_start = .;
    KEEP(*(.fini_array .fini_array.*))
    __oasis_fini_array_end = .;
  } > dmem

  .data :
  {
    *(.data .data.*)
  } > dmem

  .bss (NOLOAD) :
  {
    __bss_start = .;
    *(.bss .bss.* COMMON)
    __bss_end = .;
  } > dmem

  __oasis_heap_start = __bss_end;
  __oasis_heap_end = ORIGIN(dmem) + LENGTH(dmem) - 1;
  PROVIDE(__oasis_extmem_start = 0);
  PROVIDE(__oasis_extmem_end = 0);
  PROVIDE(__oasis_scratch_start = 0x0000);
  PROVIDE(__oasis_scratch_end = 0x0020);
  PROVIDE(__oasis_scratch_words = 0x0020);
  PROVIDE(__oasis_stack_top = ORIGIN(dmem) + LENGTH(dmem) - 1);
  PROVIDE(__stack_top = __oasis_stack_top);
}
