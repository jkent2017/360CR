#ifndef SABER_INTERFACE_H
#define SABER_INTERFACE_H

#include <Arduino.h>
#include <SoftwareSerial.h>
#include <Sabertooth.h>
#include "hardware.h"
//#include <UtilityFunctions.h>	//new and delete functions

// Interface with a sabertooth 2 channel motor controller using software serial
class SabertoothInterface {
	public:
		SabertoothInterface(byte address, int rxPin, int txPin);
		~SabertoothInterface();

		void initialize(int baudRate);
		
		// command motors using range [0,255]
		void driveTurn(unsigned char drive, unsigned char turn, bool invertDrive, bool invertTurn);

		// command motors using range [-1,1]
		void driveTurn(float driveVal, float turnVal, bool invertDrive, bool invertTurn);

		void setEStop(byte stop);
	private:
		unsigned char deadband;
		SoftwareSerial swSerial;
		Sabertooth ST;

		unsigned char checkDeadband(unsigned char value);
		char floatToByte(float floatVal);
};
#endif
