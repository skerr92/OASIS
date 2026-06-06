#ifndef OASIS_RUNTIME_H
#define OASIS_RUNTIME_H

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

int __cxa_guard_acquire(unsigned int *guard);
void __cxa_guard_release(unsigned int *guard);
void __cxa_guard_abort(unsigned int *guard);
void __cxa_pure_virtual(void) __attribute__((noreturn));

#ifdef __cplusplus
}
#endif

#endif
