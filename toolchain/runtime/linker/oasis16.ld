OUTPUT_ARCH(oasis16)
ENTRY(_start)

MEMORY
{
  imem (rx)  : ORIGIN = 0x0000, LENGTH = 0x0100
  dmem (rw)  : ORIGIN = 0x0100, LENGTH = 0x0200
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

  PROVIDE(__stack_top = ORIGIN(dmem) + LENGTH(dmem) - 1);
}
