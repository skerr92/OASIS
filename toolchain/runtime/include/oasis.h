#ifndef OASIS_RUNTIME_H
#define OASIS_RUNTIME_H

#ifdef __cplusplus
extern "C" {
#endif

void __oasis_exit(void) __attribute__((noreturn));
void __oasis_abort(void) __attribute__((noreturn));

#ifdef __cplusplus
}
#endif

#endif
