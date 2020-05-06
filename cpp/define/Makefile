CC = g++
objects = main.o TestClass.o 	#变量赋值

test_def : $(objects) 	#生成test_def
	$(CC) -o test_def $(objects)


main.o : main.cpp TestClass.h 	#依赖关系
	$(CC) -c main.cpp
TestClass.o : Define.h 	#make自动推导依赖关系（同名的.h和.cpp文件可自动推导）

#.PHONY:	clean
clean:	
	-rm test_def $(objects)