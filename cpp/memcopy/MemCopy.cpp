#include <iostream>

using namespace std;

struct TestClass
{
	TestClass(int){}
	TestClass(const TestClass& a){cout << "fff" << endl;}
	~TestClass(){}
};

int main()
{
	//������û��ʵ��Copy Elision��������fff����Ϊ����ʱ����10��������a
	TestClass a = 10;
	return 0;
}
