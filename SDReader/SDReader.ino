/*
  SD card read/write

  This example shows how to read and write data to and from an SD card file
  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

  created   Nov 2010
  by David A. Mellis
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

*/

#include <Sabertooth.h>
#include <SPI.h>
#include <SD.h>

Sabertooth ST(128);

File myFile;
byte buff;
char c[3];

struct {
  byte sync1 = 0;
  byte sync2 = 0;
  byte sync3 = 0;
  byte driveChar = 0;
  byte turnChar = 0;
  byte digital1 = 0;
  byte digital2 = 0;
} packet;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  ST.drive(0);
  ST.turn(0);

  delay(1000);

  Serial.print("Initializing SD card...");

  while (!SD.begin(4)) {
    Serial.println("initialization failed!");
    delay(500);
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  //  myFile = SD.open("path.txt", FILE_WRITE);
  //
  //  // if the file opened okay, write to it:
  //  if (myFile) {
  //    Serial.print("Writing to test.txt...");
  //    myFile.println("testing 1, 2, 3.");
  //    // close the file:
  //    myFile.close();
  //    Serial.println("done.");
  //  } else {
  //    // if the file didn't open, print an error:
  //    Serial.println("error opening test.txt");
  //  }

  // re-open the file for reading:
  myFile = SD.open("path.txt");
  if (myFile) {
    Serial.println("path.txt:");

    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      for (int ii = 0; ii < 7; ii++) {
        for (int jj = 0; jj < 4; jj++) {
          c[jj] = myFile.read();
          if (c[jj] == ' ' || c[jj] == '\n') {
            //Store Value
            switch (ii) {
              case 0:
                packet.sync1 = (byte)atoi(c);
                break;
              case 1:
                packet.sync2 = (byte)atoi(c);
                break;
              case 2:
                packet.sync3 = (byte)atoi(c);
                break;
              case 3:
                packet.driveChar = (byte)atoi(c);
                break;
              case 4:
                packet.turnChar = (byte)atoi(c);
                break;
              case 5:
                packet.digital1 = (byte)atoi(c);
                break;
              case 6:
                packet.digital2 = (byte)atoi(c);
                break;
            }
            if (c[jj] == '\n') {
              ii = 7;
            }
            break;
          }
        }
      }
      if(vroom())
        killRobot();
//      printPacket();
      //      Serial.write(myFile.read());
    }
    // close the file:
    killRobot();
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
}

void loop() {
  // nothing happens after setup
  Serial.println("Loop");
  delay(5000);
}

void printPacket() {
  Serial.print(packet.sync1, DEC);
  Serial.print(' ');
  Serial.print(packet.sync2, DEC);
  Serial.print(' ');
  Serial.print(packet.sync3, DEC);
  Serial.print(' ');
  Serial.print(packet.driveChar, DEC);
  Serial.print(' ');
  Serial.print(packet.turnChar, DEC);
  Serial.print(' ');
  Serial.print(packet.digital1, DEC);
  Serial.print(' ');
  Serial.println(packet.digital2);
}

int vroom(){
  Serial.println("vroom");
  ST.drive(packet.driveChar);
  ST.turn(packet.turnChar);
  if (1)
    return 0;
  else
    return 1; //Error flag when needed.
  
}

void killRobot(){
  ST.motor(1, 0);    // Stop.
  ST.motor(2, 0);    // Stop.
  myFile.close();
  while(1) {
    Serial.println("Mistakes have been made");
    delay(3000);
  }
}
