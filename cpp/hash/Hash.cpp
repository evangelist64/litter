#include <iostream>
#include <string>

using namespace std;

unsigned int getHash(string s)
{
	unsigned int hash = 0;
	for(unsigned int i=0; i<s.size(); i++)
	{
		hash += s[i];
	}
	return hash;
}

int main()
{
	cout << getHash("fock101") <<endl;
	return 0;
}

