; OASIS Base-16T libgcc target helpers.
;
; libgcc builds this file once per LIB1ASMFUNC with -DL_<name>.

        .section .text.libgcc, "ax"

#ifdef L_mulhi3
        .global __mulhi3
__mulhi3:
        MVV r1, r4
        MLT r1, r5
        RET
#endif

#ifdef L_ashlhi3
        .global __ashlhi3
__ashlhi3:
        MVV r1, r4
        MVI r2, 0
__ashlhi3_loop:
        JEQ r5, r2, __ashlhi3_done
        SHL r1, 1
        SBI r5, 1
        JMP __ashlhi3_loop
__ashlhi3_done:
        RET
#endif

#ifdef L_lshrhi3
        .global __lshrhi3
__lshrhi3:
        MVV r1, r4
        MVI r2, 0
__lshrhi3_loop:
        JEQ r5, r2, __lshrhi3_done
        SHR r1, 1
        SBI r5, 1
        JMP __lshrhi3_loop
__lshrhi3_done:
        RET
#endif

#ifdef L_udivhi3
        .global __udivhi3
__udivhi3:
        MVI r1, 0
        MVV r2, r4
        MVI r3, 0
        JEQ r5, r3, __udivhi3_abort
__udivhi3_loop:
        JLTU r2, r5, __udivhi3_done
        SUB r2, r5
        ADI r1, 1
        JMP __udivhi3_loop
__udivhi3_done:
        RET
__udivhi3_abort:
        JMP __oasis_abort
#endif

#ifdef L_umodhi3
        .global __umodhi3
__umodhi3:
        MVV r1, r4
        MVI r2, 0
        JEQ r5, r2, __umodhi3_abort
__umodhi3_loop:
        JLTU r1, r5, __umodhi3_done
        SUB r1, r5
        JMP __umodhi3_loop
__umodhi3_done:
        RET
__umodhi3_abort:
        JMP __oasis_abort
#endif

#ifdef L_divhi3
        .global __divhi3
__divhi3:
        MVI r1, 0
        MVI r2, 0
        MVI r3, 1
        JGE r4, r2, __divhi3_lhs_positive
        NOT r4
        ADI r4, 1
        XOR r1, r3
__divhi3_lhs_positive:
        JGE r5, r2, __divhi3_rhs_positive
        NOT r5
        ADI r5, 1
        XOR r1, r3
__divhi3_rhs_positive:
        MVV r6, r1
        MVI r1, 0
        MVV r7, r4
        JEQ r5, r2, __divhi3_abort
__divhi3_loop:
        JLTU r7, r5, __divhi3_finish
        SUB r7, r5
        ADI r1, 1
        JMP __divhi3_loop
__divhi3_finish:
        JEQ r6, r2, __divhi3_done
        NOT r1
        ADI r1, 1
__divhi3_done:
        RET
__divhi3_abort:
        JMP __oasis_abort
#endif

#ifdef L_modhi3
        .global __modhi3
__modhi3:
        MVI r1, 0
        MVI r2, 0
        MVI r3, 1
        JGE r4, r2, __modhi3_lhs_positive
        NOT r4
        ADI r4, 1
        MVV r1, r3
__modhi3_lhs_positive:
        JGE r5, r2, __modhi3_rhs_positive
        NOT r5
        ADI r5, 1
__modhi3_rhs_positive:
        MVV r6, r1
        MVV r1, r4
        JEQ r5, r2, __modhi3_abort
__modhi3_loop:
        JLTU r1, r5, __modhi3_finish
        SUB r1, r5
        JMP __modhi3_loop
__modhi3_finish:
        JEQ r6, r2, __modhi3_done
        NOT r1
        ADI r1, 1
__modhi3_done:
        RET
__modhi3_abort:
        JMP __oasis_abort
#endif
