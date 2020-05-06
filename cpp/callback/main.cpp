#include <stdio.h>

void callback()
{
	printf("ffff");
}

void func(void (*cb)())
{
	cb();
}

int main()
{
	func(callback);
	return 0;
}
