#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

template<class A>
class TempClass
{
public:
	A create()
	{
		return A();
	}
};

class MyClass
{
public:
	MyClass(){i=1;cout<<"MyClass create"<<endl;}
	~MyClass(){cout<<"MyClass destroy"<<endl;}
	void printself(){cout<<i<<endl;}
private:
	int i;
};

typedef TempClass<MyClass *> TEMP_CLASS;
int main()
{
	//MyClass();
	
	TEMP_CLASS tc;
	MyClass* p = tc.create();
	p->printself();
}
