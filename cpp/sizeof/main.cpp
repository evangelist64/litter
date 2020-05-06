#include <iostream>
#include <string>
#include <stdio.h>

using namespace std;

struct MyStruct
{
	char cc[100];
	
	MyStruct(int){}
	~MyStruct(){}
};

int main()
{
	
	char c[100];
	string s = "°²¸§Íß·¢ÎÒ";
	
	cout << sizeof(unsigned short) << endl;
	cout << sizeof(bool) << endl;
	cout << sizeof(c) << endl;
	cout << sizeof(MyStruct) << endl;
	cout << sizeof(&c) << endl;
	cout << sizeof(s) << endl;
	cout << s.length() << endl;
		
	return 0;
}
