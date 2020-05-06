#include <iostream>

using namespace std;

struct TestClass
{
	int a;
	int b;
	int c;
	
	TestClass(){}
	~TestClass(){}
};

int main()
{
	char a[100];
	TestClass tc1;
	TestClass tc2;
	tc1.a = 1;
	tc1.b = 2;
	tc1.c = 3;
	
	memcpy(a, (char*)&tc1, sizeof(TestClass));
	cout << a <<endl;
	memcpy(&tc2, a, sizeof(TestClass));
	cout << tc2.b <<endl;
}

