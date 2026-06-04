cat <<EOF
OUTPUT_FORMAT("elf32-oasis16")
OUTPUT_ARCH(oasis16)
ENTRY(_start)

MEMORY
{
  imem (rx)  : ORIGIN = 0x0000, LENGTH = 0x0100
  dmem (rw)  : ORIGIN = 0x0000, LENGTH = 0x0200
}

SECTIONS
{
  .text 0x0000 :
  {
    *(.text.start)
    *(.text .text.*)
  } > imem

  .rodata :
  {
    *(.rodata .rodata.*)
  } > dmem

  .data :
  {
    __data_start = .;
    *(.data .data.*)
    __data_end = .;
  } > dmem

  .bss :
  {
    __bss_start = .;
    *(.bss .bss.*)
    *(COMMON)
    __bss_end = .;
  } > dmem

  .stack (NOLOAD) :
  {
    __stack_start = .;
    . = ORIGIN(dmem) + LENGTH(dmem);
    __stack_end = .;
  } > dmem
}
EOF
