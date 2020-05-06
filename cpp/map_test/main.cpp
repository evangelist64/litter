#include <iostream>
#include <map>
#include <time.h>
#include <string>
using namespace std;

class MyClass
{
public:
	int a;
};

int main()
{
	map<int,MyClass*> map_1;
	for(int i=0; i<100; i++)
	{
		MyClass* mc = new MyClass();
		mc->a = i;
		map_1.insert(std::make_pair(i,mc));
	}
	map<int,MyClass*>::iterator iter = map_1.find(10);
	map_1.erase(10);
	
	if(iter != map_1.end())
	{
		MyClass* mc = iter->second;
		cout << mc->a << endl;
	}
	return 0;
}
