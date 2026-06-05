unsigned pick(unsigned a, unsigned b)
{
  if (a < b)
    return b;
  return a;
}

unsigned main(void)
{
  return pick(1, 2);
}
