(define_predicate "oasis16_simm6_operand"
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), -32, 31)")))

(define_predicate "oasis16_uimm6_operand"
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), 0, 63)")))

(define_predicate "oasis16_uimm16_operand"
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), 0, 65535)")))

(define_predicate "oasis16_memory_operand"
  (and (match_code "mem")
       (match_test "oasis16_legitimate_address_p(mode, XEXP(op, 0), false)")))
