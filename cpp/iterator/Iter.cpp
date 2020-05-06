#include <iostream>
#include <string>
#include <list>
#include <vector>

using namespace std;

int main()
{
	list<int> int_list;
	for(int i=0; i<5; i++)
	{
		int_list.push_back(i);
	}
	
	for(list<int>::iterator iter=int_list.begin(); iter!=int_list.end(); iter++)
	{
		cout << *iter << endl;
		list<int>::iterator iter_next = iter;
		while(int_list.end()!=iter_next++)
		{
			if(iter_next==int_list.end())
			{
				break;
			}
			if(*iter_next == 2)
			{
				iter_next = int_list.erase(iter_next);
			}
			cout << *iter_next << endl;
		}
	}
	return 0;
}

