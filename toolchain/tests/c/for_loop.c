unsigned main(void)
{
  unsigned i;
  unsigned acc = 0;

  for (i = 0; i < 4; i += 1)
    acc += i;

  return acc;
}
