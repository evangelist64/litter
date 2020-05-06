#include <stdio.h>
#include "Define.h"

class TestClass
{
public:
	TestClass() {printf("success");}

//	SINGLETON_POINTER_DEC(TestClass);
	SINGLETON_OBJ(TestClass);
};
