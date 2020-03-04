#include "SabertoothInterface.h"

//-- public methods --//
SabertoothInterface::SabertoothInterface(byte address, int rxPin, int txPin)
	:swSerial(rxPin, txPin), ST(address, swSerial)
{
	pinMode(stEStop, OUTPUT);
}

SabertoothInterface::~SabertoothInterface() { }

void SabertoothInterface::initialize(int baudRate)
{
	deadband = 5;
	swSerial.begin(baudRate);
	ST.autobaud();
}

void SabertoothInterface::driveTurn(unsigned char drive, unsigned char turn, bool invertDrive, bool invertTurn)
{
	drive = checkDeadband(drive); turn = checkDeadband(turn);
	char sgnDrive = (char)((int)drive - 127); char sgnTurn = (char)((int)turn - 127);
	sgnDrive = invertDrive ? -1 * sgnDrive : sgnDrive;
	sgnTurn  = invertTurn  ? -1 * sgnTurn  : sgnTurn;
	ST.drive(sgnDrive); ST.turn(sgnTurn);
}

void SabertoothInterface::driveTurn(float driveVal, float turnVal, bool invertDrive, bool invertTurn)
{
	// to be implemented
	char sgnDrive = floatToByte(driveVal); char sgnTurn = floatToByte(turnVal);
	sgnDrive = invertDrive ? -1 * sgnDrive : sgnDrive;
	sgnTurn = invertTurn ? -1 * sgnTurn : sgnTurn;
	ST.drive(sgnDrive); ST.turn(sgnTurn);

	//Serial.print(sgnDrive, DEC); Serial.print(" <> "); Serial.println(sgnTurn, DEC);
}

// if stop is true, throws estop, else sets it high
void SabertoothInterface::setEStop(byte stop)
{
	//Serial.print("Set estop: "); Serial.println(!stop);
	digitalWrite(stEStop, !stop);
}

//-- private methods --//
unsigned char SabertoothInterface::checkDeadband(unsigned char value)
{
	if (value < 127 + deadband && value > 127 - deadband) { return 127; }
	return value;
}

char SabertoothInterface::floatToByte(float floatVal)
{
	return (char)(floatVal * 127);
}