#include <stdio.h> 

long int count = 0;
void func() {
  char msg[1024];
  printf("count: %ld\n", count++);
  func();
}

int main(void) 
{
  func();
  return 0;
}
