#include <iostream>
#include <vector>
#include <time.h>
#include <string>
using namespace std;

class MyClass
{
	public int a;
};

void printCurTime()
{
	time_t t = time(0);
	cout<<t<<endl;
}

int main()
{
	vector<MyClass*> vec_1;
	vector<MyClass*> vec_2;

	printCurTime();
	for(int i=0; i<100; i++)
	{
		vec_1.push_back(new MyClass());
	}
	printCurTime();
	
	//vec_2 = vec_1;
	//vec_2.assign(vec_1.begin(),vec_1.end());
	//for(vector<MyClass*>::iterator iter=vec_1.begin();iter!=vec_1.end();iter++)
	//{
	//	vec_2.push_back(*iter);
	//}
	printCurTime();
	
	cout << &vec_1 << "|" << &vec_2<<endl;
	cout << &vec_1[1] << "|" << &vec_2[1]<<endl;

	return 0;
}
