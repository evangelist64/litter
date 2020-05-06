#include <iostream>
#include <string>

using namespace std;

int main()
{
	unsigned int a = 4294967295;
	for(int i=0;i<3;i++)
	{
		cout << a++ <<endl;
	}

	int b = 2147483647;
	for(int i=0;i<3;i++)
	{
		cout << b++ <<endl;
	}
	return 0;
}

