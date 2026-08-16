#ifndef OASIS_RUNTIME_H
#define OASIS_RUNTIME_H

#define OASIS16_ADDRESS_MASK 0x7fffU
#define OASIS16_MMIO_BIT 0x8000U
#define OASIS16_MEM_ADDRESS(word) ((unsigned int)(word) & OASIS16_ADDRESS_MASK)
#define OASIS16_MMIO_ADDRESS(word) \
  (OASIS16_MMIO_BIT | ((unsigned int)(word) & OASIS16_ADDRESS_MASK))
#define OASIS16_MEM_PTR(type, word) ((type *)OASIS16_MEM_ADDRESS(word))
#define OASIS16_MMIO_PTR(type, word) ((volatile type *)OASIS16_MMIO_ADDRESS(word))

#ifdef __cplusplus
extern "C" {
#endif

void __oasis_exit(void) __attribute__((noreturn));
void __oasis_abort(void) __attribute__((noreturn));

extern void (*__oasis_init_array_start[])(void);
extern void (*__oasis_init_array_end[])(void);
extern void (*__oasis_fini_array_start[])(void);
extern void (*__oasis_fini_array_end[])(void);

extern unsigned int __oasis_extmem_start;
extern unsigned int __oasis_extmem_end;
extern unsigned int __oasis_heap_start;
extern unsigned int __oasis_heap_end;
extern unsigned int __oasis_stack_top;
extern unsigned int __oasis_scratch_start;
extern unsigned int __oasis_scratch_end;
extern unsigned int __oasis_scratch_words;

int __cxa_guard_acquire(unsigned int *guard);
void __cxa_guard_release(unsigned int *guard);
void __cxa_guard_abort(unsigned int *guard);
void __cxa_pure_virtual(void) __attribute__((noreturn));

#ifdef __cplusplus
}
#endif

#endif
