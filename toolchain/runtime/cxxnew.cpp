#include <stddef.h>

extern "C" void __oasis_abort(void) __attribute__((noreturn));

void *operator new(size_t) __attribute__((weak));
void *operator new(size_t)
{
    __oasis_abort();
}

void *operator new[](size_t) __attribute__((weak));
void *operator new[](size_t)
{
    __oasis_abort();
}

void operator delete(void *) noexcept __attribute__((weak));
void operator delete(void *) noexcept
{
}

void operator delete[](void *) noexcept __attribute__((weak));
void operator delete[](void *) noexcept
{
}

void operator delete(void *, size_t) noexcept __attribute__((weak));
void operator delete(void *, size_t) noexcept
{
}

void operator delete[](void *, size_t) noexcept __attribute__((weak));
void operator delete[](void *, size_t) noexcept
{
}
