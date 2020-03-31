#include <SoftwareSerial.h>
#include <Sabertooth.h>
#include <SPI.h>
#include <Ethernet.h>
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 177);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
int port = 8888;

SoftwareSerial SabertoothSerial(NOT_A_PIN, 18);
Sabertooth ST(128, SabertoothSerial);
EthernetServer server(port);
EthernetClient client;

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
  bool digital1 = 0;
  byte digital2 = 0;
} packet;

void setup() {
  Serial.begin(9600);
  SabertoothSerial.begin(9600);
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  server.begin();
  ST.drive(0);
  ST.turn(0);
}

void loop() {
  client = server.available();
  if (client.available()) {
    for (int ii = 0; ii < 7; ii++) {
      for (int jj = 0; jj < 5; jj++) {
        delay(1);
        c[jj] = client.read();
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
    if (packet.sync1 == 1 && packet.sync2 == 2 && packet.sync3 == 3) {
      if (packet.digital1)
        killRobot();
      else
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
  ST.drive(packet.driveChar);
  ST.turn(packet.turnChar);
}

void killRobot() {
  ST.motor(1, 0);    // Stop.
  ST.motor(2, 0);    // Stop.
}
