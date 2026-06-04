; OASIS Base-16T bare-metal startup.
;
; The linker places this file first so _start is instruction 0. Platform code may
; override __stack_top in the linker script when a core has a different
; data-memory size.

        .section .text.startup, "ax"
        .global _start
        .global __oasis_exit
        .global __oasis_abort

_start:
        MVI r56, __stack_top
        CALL main

__oasis_exit:
        JMP __oasis_exit

__oasis_abort:
        JMP __oasis_abort
