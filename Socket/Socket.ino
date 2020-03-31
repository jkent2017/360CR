#include <SPI.h>
#include <Ethernet.h>
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 177);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
int port = 8888;

EthernetServer server(port);
boolean alreadyConnected = false; // whether or not the client was connected previously
EthernetClient client;

void setup() {
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  Serial.begin(9600);
  server.begin();
}

void loop() {
  // wait for a new client:
  client = server.available();
  if (client.available() > 0) {
    char thisChar = client.read();
    Serial.print(thisChar);
  }
}
