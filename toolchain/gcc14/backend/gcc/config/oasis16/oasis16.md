(define_constants
  [
    (R1 1)
    (R58 58)
  ])

(include "constraints.md")
(include "predicates.md")

(define_attr "type" "alu,load,store,branch,call" (const_string "alu"))

(define_insn "nop"
  [(const_int 0)]
  ""
  "NOP"
  [(set_attr "type" "alu")])

(define_expand "prologue"
  [(const_int 0)]
  ""
  {
    oasis16_expand_prologue();
    DONE;
  })

(define_expand "epilogue"
  [(const_int 0)]
  ""
  {
    oasis16_expand_epilogue();
    DONE;
  })

(define_insn "movhi"
  [(set (match_operand:HI 0 "nonimmediate_operand" "=r,r,r,m")
        (match_operand:HI 1 "general_operand" "r,I,m,r"))]
  ""
  "@
   MVV %0, %1
   MVI %0, %1
   LDR %0, %1
   STR %1, %0"
  [(set_attr "type" "alu,alu,load,store")])

(define_insn "addhi3"
  [(set (match_operand:HI 0 "register_operand" "=r,r")
        (plus:HI (match_operand:HI 1 "register_operand" "0,0")
                 (match_operand:HI 2 "nonmemory_operand" "r,I")))]
  ""
  "@
   ADD %0, %2
   ADI %0, %2")

(define_insn "subhi3"
  [(set (match_operand:HI 0 "register_operand" "=r,r")
        (minus:HI (match_operand:HI 1 "register_operand" "0,0")
                  (match_operand:HI 2 "nonmemory_operand" "r,I")))]
  ""
  "@
   SUB %0, %2
   SBI %0, %2")

(define_insn "andhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (and:HI (match_operand:HI 1 "register_operand" "0")
                (match_operand:HI 2 "register_operand" "r")))]
  ""
  "AND %0, %2")

(define_insn "iorhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (ior:HI (match_operand:HI 1 "register_operand" "0")
                (match_operand:HI 2 "register_operand" "r")))]
  ""
  "OOR %0, %2")

(define_insn "xorhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (xor:HI (match_operand:HI 1 "register_operand" "0")
                (match_operand:HI 2 "register_operand" "r")))]
  ""
  "XOR %0, %2")

(define_insn "one_cmplhi2"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (not:HI (match_operand:HI 1 "register_operand" "0")))]
  ""
  "NOT %0")

(define_insn "mulhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (mult:HI (match_operand:HI 1 "register_operand" "0")
                 (match_operand:HI 2 "register_operand" "r")))]
  ""
  "MLT %0, %2")

(define_insn "ashlhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (ashift:HI (match_operand:HI 1 "register_operand" "0")
                   (match_operand:HI 2 "oasis16_uimm6_operand" "J")))]
  ""
  "SHL %0, %2")

(define_insn "lshrhi3"
  [(set (match_operand:HI 0 "register_operand" "=r")
        (lshiftrt:HI (match_operand:HI 1 "register_operand" "0")
                     (match_operand:HI 2 "oasis16_uimm6_operand" "J")))]
  ""
  "SHR %0, %2")

(define_insn "returner"
  [(return)]
  ""
  "RET"
  [(set_attr "type" "branch")])

(define_insn "jump"
  [(set (pc)
        (label_ref (match_operand 0 "" "")))]
  ""
  "JMP %0"
  [(set_attr "type" "branch")])

(define_insn "indirect_jump"
  [(set (pc)
        (match_operand:HI 0 "register_operand" "r"))]
  ""
  "JMR %0"
  [(set_attr "type" "branch")])

(define_expand "call"
  [(parallel [(call (match_operand:HI 0 "oasis16_call_operand" "")
                    (match_operand 1 "" ""))
              (clobber (reg:HI R58))])]
  ""
  "")

(define_insn "*call"
  [(call (mem:HI (match_operand:HI 0 "oasis16_call_address_operand" "S"))
         (match_operand 1 "" ""))
   (clobber (reg:HI R58))]
  ""
  "CALL %0"
  [(set_attr "type" "call")])

(define_insn "*call_no_clobber"
  [(call (mem:HI (match_operand:HI 0 "oasis16_call_address_operand" "S"))
         (match_operand 1 "" ""))]
  ""
  "CALL %0"
  [(set_attr "type" "call")])

(define_expand "call_value"
  [(parallel [(set (match_operand 0 "register_operand" "")
                   (call (match_operand:HI 1 "oasis16_call_operand" "")
                         (match_operand 2 "" "")))
              (clobber (reg:HI R58))])]
  ""
  "")

(define_insn "*call_value"
  [(set (match_operand 0 "register_operand" "=r")
        (call (mem:HI (match_operand:HI 1 "oasis16_call_address_operand" "S"))
              (match_operand 2 "" "")))
   (clobber (reg:HI R58))]
  ""
  "CALL %1"
  [(set_attr "type" "call")])

(define_insn "*call_value_no_clobber"
  [(set (match_operand 0 "register_operand" "=r")
        (call (mem:HI (match_operand:HI 1 "oasis16_call_address_operand" "S"))
              (match_operand 2 "" "")))]
  ""
  "CALL %1"
  [(set_attr "type" "call")])

(define_insn "cbranchhi4"
  [(set (pc)
        (if_then_else
          (match_operator 0 "comparison_operator"
            [(match_operand:HI 1 "register_operand" "r")
             (match_operand:HI 2 "register_operand" "r")])
          (label_ref (match_operand 3 "" ""))
          (pc)))]
  ""
  "*
   switch (GET_CODE (operands[0]))
     {
	     case EQ: return \"JEQ %1, %2, %3\";
	     case NE: return \"JNE %1, %2, %3\";
	     case LT: return \"JLT %1, %2, %3\";
	     case GE: return \"JGE %1, %2, %3\";
	     case GT: return \"JLT %2, %1, %3\";
	     case LE: return \"JGE %2, %1, %3\";
	     case LTU: return \"JLTU %1, %2, %3\";
	     case GEU: return \"JGEU %1, %2, %3\";
	     case GTU: return \"JLTU %2, %1, %3\";
	     case LEU: return \"JGEU %2, %1, %3\";
	     default: gcc_unreachable ();
	     }"
  [(set_attr "type" "branch")])
