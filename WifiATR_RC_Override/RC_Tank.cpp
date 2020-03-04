#include "RC_Tank.h"

// public methods //
RC_Tank::RC_Tank(int _drivePin, int _turnPin, int _modePin, int _sparePin)
{
	drivePin = _drivePin; turnPin = _turnPin;
	modePin = _modePin; sparePin = _sparePin;

	// slope/intercept for converting RC signal to range [-1,1]
	mFloat = (float)2 / (pulseHigh - pulseLow);
	bFloat = -1 * pulseLow*mFloat;

	// slope/intercept for converting [-1,1] to [-127,127]
	mByte = (float)255 / (1 - 0);
	bByte = 0;
}

RC_Tank::~RC_Tank() {}

// Reads RC values ~[1000,2000] and returns them as floats in range [-1,1]
bool RC_Tank::GetDriveTurn(float& drive, float& turn, float& mode, float& spare)
{
	// Read in the RC pulses
	unsigned long DRIVE_PULSE_WIDTH = pulseIn(drivePin, HIGH, PULSEIN_TIMEOUT);
	unsigned long TURN_PULSE_WIDTH = pulseIn(turnPin, HIGH, PULSEIN_TIMEOUT);
	unsigned long MODE_PULSE_WIDTH = pulseIn(modePin, HIGH, PULSEIN_TIMEOUT);
	unsigned long SPARE_PULSE_WIDTH = pulseIn(sparePin, HIGH, PULSEIN_TIMEOUT);
	/*
	Serial.print("RC Stuff: ");
	Serial.print(DRIVE_PULSE_WIDTH); Serial.print(" :: ");
	Serial.print(TURN_PULSE_WIDTH); Serial.print(" :: ");
	Serial.print(MODE_PULSE_WIDTH); Serial.print(" :: ");
	Serial.println(SPARE_PULSE_WIDTH);
	*/
	// If pulses too short, throw sabertooth estop
	if (DRIVE_PULSE_WIDTH < 500 || TURN_PULSE_WIDTH < 500 || MODE_PULSE_WIDTH < 500) {
		return false;
	}

	// convert RC signals to continuous values from [-1,1]
	drive = convertRCtoFloat(DRIVE_PULSE_WIDTH);
	turn = -1 * convertRCtoFloat(TURN_PULSE_WIDTH);
	mode = convertRCtoFloat(MODE_PULSE_WIDTH);
	spare = convertRCtoFloat(SPARE_PULSE_WIDTH);

	return true;
}

bool RC_Tank::GetMode(float& mode)
{
	unsigned long MODE_PULSE_WIDTH = pulseIn(modePin, HIGH, PULSEIN_TIMEOUT);
	// If pulses too short, throw sabertooth estop
	if (MODE_PULSE_WIDTH < 500) {
		return false;
	}

	mode = convertRCtoFloat(MODE_PULSE_WIDTH);
}

// private methods //
float RC_Tank::convertRCtoFloat(unsigned long pulseWidth)
{
	// deadband
	if (pulseWidth > 1450 && pulseWidth < 1550) { pulseWidth = (float)(pulseHigh + pulseLow) / 2; }

	float checkVal = mFloat*pulseWidth + bFloat - 1;
	checkVal = checkVal < -1 ? -1 : checkVal;
	checkVal = checkVal >  1 ? 1 : checkVal;

	return checkVal;
}