#include <iostream>
#include <thread>
#include <chrono>
using namespace std;

long int count = 0;
void stack_alloc() {
  char msg[102400];
  cout<<"count:"<<count<<endl;
  count++;
  this_thread::sleep_for(chrono::seconds(1));
  stack_alloc();
}

void my_fun()
{
	while(1)
	{
		cout<<"fff"<<endl;
		this_thread::sleep_for(chrono::seconds(1));
	}
}

int main()
{
//	thread t1(my_fun);
//	t1.join();
//	t1.detach();

	thread t2(stack_alloc);
	while(1)
	{
		cout<<"ggg"<<endl;
		this_thread::sleep_for(chrono::seconds(1));
	}
	return 0;
}
