#include <SPI.h>
#include <Ethernet2.h>
#include "SoftwareSerial.h"
#include "Sabertooth.h"
#include "hardware.h"
#include "WifiATRInterface.h"
#include "SabertoothInterface.h"
#include "UtilityFunctions.h"
#include "RC_Tank.h"

// Network stuff
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xC0, 0xF3 };
byte ip[] = { 192, 168, 1, 57 };
byte gateway[] = { 192, 168, 1, 1 };
int port = 5050;

WifiATRInterface wifiInterface(mac, ip, port, gateway);
SabertoothInterface stInterface(stAddress, NOT_A_PIN, stTxPin);

//connection loss timeout
volatile int rxTimeoutCounter = 0;
int rxTimeoutTime = 10;	//1 second timeout on 10 Hz timer

//24V battery monitoring
int battery24Voltage = 0;

// RC controller
RC_Tank rcTank(drivePinRC, turnPinRC, modePinRC, sparePinRC);

//track input source
enum OPERATION_STATES{ WIFI = 0, RC = 1 };
OPERATION_STATES operationState = WIFI, prev_operationState = RC;

void setup()
{
	Serial.begin(9600); Serial1.begin(9600);
	wifiInterface.startEthernetServer();
	stInterface.initialize(stBaud);
	initTimer();

	// set relay pins as outputs
	pinMode(output1, OUTPUT); pinMode(output2, OUTPUT);
	pinMode(output3, OUTPUT); pinMode(output4, OUTPUT);
}

void initTimer()
{
	// initialize timer1 with 10 Hz frequnecy
	noInterrupts();           // disable all interrupts
	TCCR1A = 0;
	TCCR1B = 0;
	TCNT1 = 0;

	//OCR1A = 31250;            // compare match register 16MHz/256/2Hz
	OCR1A = 6250;            // compare match register 16MHz/256/10Hz
	TCCR1B |= (1 << WGM12);   // CTC mode
	TCCR1B |= (1 << CS12);    // 256 prescaler 
	TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt
	interrupts();             // enable all interrupts
}

// timer1 interrupt
ISR(TIMER1_COMPA_vect)          // timer compare interrupt service routine
{
	rxTimeoutCounter++;
	if (rxTimeoutCounter > 100) { rxTimeoutCounter = 100; }
}

void loop()
{
	// Switch control source based on operation state //
	OPERATION_STATES next_operationState = operationState;
	switch (operationState) {
		case WIFI: {
			//-- ENTRY --//
			if (prev_operationState != WIFI) {
				Serial.println("Entered WIFI state");
				allStop();
				stInterface.setEStop(false);
			}

			//-- ACTIONS --//
			// Update battery voltage
			battery24Voltage = analogRead(batt24VInput) >> 2;
			wifiInterface.updateAnalogs((battery24Voltage & 0xFF), 0, 0);

			// Check if a packet was received
			bool packetReceived = wifiInterface.checkForPacket();
			if (packetReceived) {
				rxTimeoutCounter = 0;
				//debugPrintRxPacket();
			}

			// Check for rx timeout
			checkRxTimeout();

			// Command Motors
			stInterface.driveTurn(wifiInterface.rxPacket.driveChar, wifiInterface.rxPacket.turnChar, false, true);

			// Control Relays
			relayControl(wifiInterface.rxPacket.digital_1);

			//-- TRANSITIONS --//
			// Check RC MODE input
			float mode;
			bool success = rcTank.GetMode(mode);

			if (success && mode > -0.7) { next_operationState = RC; }

			break;
		}
		case RC: {
			//-- ENTRY --//
			if (prev_operationState != RC) {
				Serial.println("Entered RC state");
				allStop();
				stInterface.setEStop(false);
			}

			//-- ACTIONS --//
			float drive, turn, mode, spare;
			bool success = rcTank.GetDriveTurn(drive, turn, mode, spare);
			if (!success) { Serial.println("Failed to read!"); allStop(); }

			// Command Motors
			stInterface.driveTurn(drive, turn, false, false);
			/*
			Serial.print("RC Stuff: ");
			Serial.print(drive); Serial.print(" :: ");
			Serial.print(turn); Serial.print(" :: ");
			Serial.print(mode); Serial.print(" :: ");
			Serial.println(spare);
			*/
			//-- TRANSITIONS --//
			// Check RC MODE input
			if (success && mode < -0.7) { next_operationState = WIFI; }

			break;
		}
	}
	prev_operationState = operationState;
	operationState = next_operationState;
	
	//delay(5);
}

void relayControl(byte digital)
{
	if (digital & f0Mask) { digitalWrite(output1, HIGH); }
	else { digitalWrite(output1, LOW); }

	if (digital & f1Mask) { digitalWrite(output2, HIGH); }
	else { digitalWrite(output2, LOW); }

	if (digital & f2Mask) { digitalWrite(output3, HIGH); }
	else { digitalWrite(output3, LOW); }

	if (digital & f3Mask) { digitalWrite(output4, HIGH); }
	else { digitalWrite(output4, LOW); }
}

void checkRxTimeout()
{
  Serial.println("Checking RxTimeout-2");
	if (rxTimeoutCounter >= rxTimeoutTime) { allStop(); }
	else { stInterface.setEStop(false); }
}

void allStop()
{
	Serial.println("Stopping");
	// stop motors
	wifiInterface.rxPacket.driveChar = 127; wifiInterface.rxPacket.turnChar = 127;
	stInterface.driveTurn((unsigned char)127, (unsigned char)127, false, false);
	stInterface.setEStop(true);

	// stop ptz camera
//	wifiInterface.rxPacket.panChar = 127; wifiInterface.rxPacket.tiltChar = 127;

	// pull other digital IO low
	wifiInterface.rxPacket.digital_1 = 0; wifiInterface.rxPacket.digital_2 = 0;
}

void debugPrintRxPacket() {
	Serial.print(wifiInterface.rxPacket.sync_1); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.sync_2); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.sync_3); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.driveChar); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.turnChar); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.panHighChar); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.panChar); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.tiltHighChar); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.tiltChar); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.digital_1); Serial.print(" ");
	Serial.print(wifiInterface.rxPacket.digital_2); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.checksumHigh); Serial.print(" ");
//	Serial.print(wifiInterface.rxPacket.checksumLow); Serial.println("");
}
