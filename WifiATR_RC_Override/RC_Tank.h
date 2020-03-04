#ifndef RC_TANK_H
#define RC_TANK_H

#include <Arduino.h>

class RC_Tank {
	public:
		RC_Tank(int _drivePin, int _turnPin, int _modePin, int _sparePin);
		~RC_Tank();

		// return values from [-1,1]
		bool GetDriveTurn(float& drive, float& turn, float& mode, float& spare);

		// get mode only
		bool GetMode(float& mode);

	private:
		int drivePin, turnPin, modePin, sparePin;
		float pulseLow = 1184, pulseHigh = 1790;
		unsigned long PULSEIN_TIMEOUT = 15000;

		float mByte, bByte;
		float mFloat, bFloat;

		float convertRCtoFloat(unsigned long pulseWidth);
};
#endif