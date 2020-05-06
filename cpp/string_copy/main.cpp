#include <iostream>
#include <string>

using namespace std;

class TestClass : public string
{
public:
	TestClass(){}
	TestClass(const string& str){cout << "fff" << endl;}
	~TestClass(){}
};

TestClass getTestClass()
{
	return TestClass("ggg");	
}	

int main()
{
	/*
	const string s = "ggggg";
	TestClass a = s;

	cout << &a << endl;
	cout << &s << endl;
	*/
	
	TestClass a = getTestClass();
	
	return 0;
}

