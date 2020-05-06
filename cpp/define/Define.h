#define SINGLETON_POINTER_DEC(class_name) public:\
	static class_name& getInstance(); \
	private:\
	static class_name* _instance_##class_name; 

#define SINGLETON_POINTER_DEF(class_name) class_name* class_name::_instance_##class_name = NULL; \
	class_name& class_name::getInstance(){ \
		if(!_instance_##class_name) \
		{ \
			_instance_##class_name = new class_name(); \
		} \
		return *_instance_##class_name; \
	};

#define SINGLETON_OBJ(class_name) public: \
	static class_name& getInstance(){ \
	static class_name obj; \
	return obj; \
	};
