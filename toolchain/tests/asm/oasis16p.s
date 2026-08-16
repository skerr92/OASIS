.text
.global oasis16p_fixture
oasis16p_fixture:
    TRAP 0x12
    ERET
    WFI
    CSRR r4, 0x01
    CSRW r5, 0x02
    CSRS r6, 0x03
    CSRC r7, 0x04
    .long 0x38011200
    .long 0x38400001
    .long 0x39c00000
