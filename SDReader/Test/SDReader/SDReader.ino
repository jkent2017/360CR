#include <Sabertooth.h>

Sabertooth ST(128);
void vroom();
void killRobot();
void printPacket();

byte buff;
char c[5];

struct {
  byte sync1 = 0;
  byte sync2 = 0;
  byte sync3 = 0;
  int8_t driveChar = 0;
  int8_t turnChar = 0;
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
}

void loop() {
  if (Serial.available()) {
    Serial.println("Check");
    for (int ii = 0; ii < 7; ii++) {
      for (int jj = 0; jj < 5; jj++) {
        c[jj] = Serial.read();
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
              packet.driveChar = (int8_t)atoi(c);
              break;
            case 4:
              packet.turnChar = (int8_t)atoi(c);
              break;
            case 5:
              packet.digital1 = (byte)atoi(c);
              break;
            case 6:
              packet.digital2 = (byte)atoi(c);
              break;
          }
          if (c[jj] == '\n')
            ii = 7;
          for (jj = 0; jj < 5; jj++)
            c[jj] = ' ';
          break;
        }
      }
    }
        printPacket();
    if (packet.sync1 == 1 && packet.sync2 == 2 && packet.sync3 == 3) {
      vroom();
      printPacket();
    }
  }
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

void vroom() {
  Serial.println("vroom");
  ST.drive(packet.driveChar);
  ST.turn(packet.turnChar);
}

void killRobot() {
  ST.motor(1, 0);    // Stop.
  ST.motor(2, 0);    // Stop.
  while (1)
    Serial.println("Mistakes have been made");
}
