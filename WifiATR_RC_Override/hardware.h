#include <Arduino.h>

// Define LED pins //
#define L1 44			// Output Status LEDs
#define L2 42
#define L3 40
#define L4 38

// RC connections to Sabertooth //
#define stAddress 128
#define stTxPin 6
#define stEStop 7
#define stBaud 9600

// Battery Monitoring Analog Input //
#define batt24VInput 0	//analog pin 1

// Output signals for TTL Relays //
#define output1 41		
#define output2 43
#define output3 45
#define output4 47

// RC Input Pins //
#define drivePinRC 4
#define turnPinRC 5
#define modePinRC 3
#define sparePinRC 2