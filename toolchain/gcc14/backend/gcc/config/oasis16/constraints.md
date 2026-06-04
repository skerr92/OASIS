(define_register_constraint "r" "GENERAL_REGS"
  "A general OASIS register.")

(define_constraint "I"
  "A 16-bit unsigned immediate."
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), 0, 65535)")))

(define_constraint "J"
  "A 6-bit unsigned immediate."
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), 0, 63)")))

(define_constraint "K"
  "A signed 6-bit offset."
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), -32, 31)")))
