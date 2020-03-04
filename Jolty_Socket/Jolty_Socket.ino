// Jolty Sample for Packet Serial
// Copyright (c) 2012 Dimension Engineering LLC
// See license.txt for license details.

#include <Sabertooth.h>
#include "server.h"

// DIP(1-6): 001111

Sabertooth ST(128); // The Sabertooth is on address 128. We'll name its object ST.
                    // If you've set up your Sabertooth on a different address, of course change
                    // that here. For how to configure address, etc. see the DIP Switch Wizard for
                    //   Sabertooth - http://www.dimensionengineering.com/datasheets/SabertoothDIPWizard/start.htm
                    //   SyRen      - http://www.dimensionengineering.com/datasheets/SyrenDIPWizard/start.htm
                    // Be sure to select Packetized Serial Mode for use with this library.
                    //
                    // On that note, you can use this library for SyRen just as easily.
                    // The diff-drive commands (drive, turn) do not work on a SyRen, of course, but it will respond correctly
                    // if you command motor 1 to do something (ST.motor(1, ...)), just like a Sabertooth.
                    //
                    // In this sample, hardware serial TX connects to S1.
                    // See the SoftwareSerial example in 3.Advanced for how to use other pins.
                                        
void setup()
{
//  SabertoothTXPinSerial.begin(9600); // 9600 is the default baud rate for Sabertooth packet serial.
  Serial.begin(9600);
//  ST.drive(0);
//  ST.turn(0);
//  ST.autobaud(); // Send the autobaud command to the Sabertooth controller(s).
                 // NOTE: *Not all* Sabertooth controllers need this command.
                 //       It doesn't hurt anything, but V2 controllers use an
                 //       EEPROM setting (changeable with the function setBaudRate) to set
                 //       the baud rate instead of detecting with autobaud.
                 //
                 //       If you have a 2x12, 2x25 V2, 2x60 or SyRen 50, you can remove
                 //       the autobaud line and save yourself two seconds of startup delay.
}


void loop()
{

  delay(1000);
  
  test1();

  while(1) {
    Serial.println("Done");
    delay(750);
    }
}

void test1() {
  Serial.println("Delay");
  delay(2000);
  Serial.println("Start");
  ST.motor(1, 127);  // Go forward at full power.
  ST.motor(2, 127);  // Go forward at full power.
  delay(2000);       // Wait 2 seconds.
  Serial.println("Stop");
  ST.motor(1, 0);    // Stop.
  ST.motor(2, 0);    // Stop.
  delay(2000);       // Wait 2 seconds.
  Serial.println("Back");
  ST.motor(1, -127); // Reverse at full power.
  ST.motor(2, -127); // Reverse at full power.
  delay(2000);       // Wait 2 seconds.
  Serial.println("Stop");
  ST.motor(1, 0);    // Stop.
  ST.motor(2, 0);    // Stop.
  delay(2000);
}

void test2() {
  Serial.println("Stop");
  ST.motor(1, 0);    // Stop.
//  ST.motor(2, 0);    // Stop.
}
