#include <oasis.h>

typedef int (*guard_acquire_fn)(unsigned int *);
typedef void (*guard_update_fn)(unsigned int *);

guard_acquire_fn guard_acquire_ref = __cxa_guard_acquire;
guard_update_fn guard_release_ref = __cxa_guard_release;
guard_update_fn guard_abort_ref = __cxa_guard_abort;

extern "C" int main(void)
{
  return 0;
}
