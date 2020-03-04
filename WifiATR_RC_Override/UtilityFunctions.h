#ifndef UTILITY_H
#define UTILITY_H

class UtilityFunctions {
	// new and delete operators
	void* operator new(size_t size){ return malloc(size); }
	void operator delete(void* ptr) { free(ptr); }

	//byte f1Mask = B00000010, f2Mask = B00000100, f3Mask = B00001000, f4Mask = B00010000;
	#define f0Mask B00000001
	#define f1Mask B00000010
	#define f2Mask B00000100
	#define f3Mask B00001000
	#define f4Mask B00010000
	#define f5Mask B00100000
	#define f6Mask B01000000
	#define f7Mask B10000000
};

#endif