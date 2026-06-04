/* First C compiler smoke-test target.
 *
 * Expected long-term behavior:
 *   oasis16-elf-gcc -ffreestanding -nostdlib -S add.c -o add.s
 */
unsigned add(unsigned a, unsigned b) {
    return a + b;
}
