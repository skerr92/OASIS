unsigned pad[768];
unsigned marker = 7;

unsigned main(void)
{
  pad[767] = marker;
  return pad[767];
}
