#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

int main()
{
	while(true)
	{
		try
		{
			throw 1;
		}
		catch(...)
		{
			cout<< "1" << endl;
		}
		cout<< "2" << endl;
	}
	return 0;
}
