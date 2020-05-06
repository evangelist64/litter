#include <iostream>
#include <string.h>

using namespace std;

int main()
{
	char c[100],d[100];
	int a = 1;
	memcpy(c,&a,sizeof(unsigned int));
	memcpy(c+4,&a,sizeof(unsigned int));
	
	cout << strlen(c) <<endl;
	strncpy(d,c,strlen(c));
	cout << d << endl;
	return 0;
}

