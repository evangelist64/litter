#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

int main()
{
	//const char* s = "fff";
	string s = "";

	char ss[255] = "gg";
	//cout<<string(s)<<endl;
	/*
	int i=0;
	for(; i<s.length(); i++)
	{
		ss[i]=s[i];
	}
	ss[i] = '\0'; */
	//cout << string(ss) << endl;
	
	cout <<sizeof(ss) <<endl;
	cout <<s.length() <<endl;
	return 0;
}
