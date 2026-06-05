unsigned sum_to(unsigned limit)
{
  unsigned i = 0;
  unsigned sum = 0;

  while (i < limit)
    {
      sum += i;
      i += 1;
    }

  return sum;
}

unsigned main(void)
{
  return sum_to(5);
}
