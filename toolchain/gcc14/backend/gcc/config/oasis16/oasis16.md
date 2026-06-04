(define_constants
  [
    (R1 1)
    (R58 58)
  ])

(define_attr "type" "alu,load,store,branch,call" (const_string "alu"))

(define_insn "movhi"
  [(set (match_operand:HI 0 "nonimmediate_operand" "=r,r,m")
        (match_operand:HI 1 "general_operand" "r,i,r"))]
  ""
  "@
   MVV %0, %1
   MVI %0, %1
   STR %1, %0")

(define_insn "addhi3"
  [(set (match_operand:HI 0 "register_operand" "=r,r")
        (plus:HI (match_operand:HI 1 "register_operand" "0,0")
                 (match_operand:HI 2 "nonmemory_operand" "r,i")))]
  ""
  "@
   ADD %0, %2
   ADI %0, %2")

(define_insn "subhi3"
  [(set (match_operand:HI 0 "register_operand" "=r,r")
        (minus:HI (match_operand:HI 1 "register_operand" "0,0")
                  (match_operand:HI 2 "nonmemory_operand" "r,i")))]
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

(define_insn "returner"
  [(return)]
  ""
  "RET"
  [(set_attr "type" "branch")])

(define_insn "call"
  [(call (match_operand:HI 0 "immediate_operand" "i")
         (match_operand 1 "" ""))]
  ""
  "CALL %0"
  [(set_attr "type" "call")])
