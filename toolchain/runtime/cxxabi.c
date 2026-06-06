#include <oasis.h>

int __attribute__((weak)) __cxa_guard_acquire(unsigned int *guard)
{
    if (*guard == 0u) {
        return 1;
    }

    return 0;
}

void __attribute__((weak)) __cxa_guard_release(unsigned int *guard)
{
    *guard = 1u;
}

void __attribute__((weak)) __cxa_guard_abort(unsigned int *guard)
{
    (void)guard;
}

void __attribute__((weak)) __cxa_pure_virtual(void)
{
    __oasis_abort();
}
