unsigned load_store(unsigned *ptr)
{
  *ptr = 0x1234;
  return *ptr;
}

unsigned main(void)
{
  unsigned value = 0;
  return load_store(&value);
}
