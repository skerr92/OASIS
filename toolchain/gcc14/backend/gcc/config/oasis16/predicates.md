(define_predicate "oasis16_simm6_operand"
  (and (match_code "const_int")
       (match_test "IN_RANGE(INTVAL(op), -32, 31)")))
