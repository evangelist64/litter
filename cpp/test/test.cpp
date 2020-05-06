#include<stdio.h>
#include<time.h>
#include<sys/time.h>
#include <sys/timeb.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int main()
{
	struct timeb timebuffer;
	ftime(&timebuffer);
	int utc_to_local = 60*timebuffer.timezone*(-1);
	printf("%d\n",timebuffer.time);
	printf("%d\n",utc_to_local);
	return 0;
}

