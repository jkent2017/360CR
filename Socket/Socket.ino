#include <SPI.h>
#include <Ethernet2.h>

byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0xC0, 0xF3 };
byte ip[] = {10, 0, 0, 177};
byte server[] = { 127, 0, 0, 1 };
int port = 5050;

EthernetClient client;

void setup() {
  Ethernet.begin(mac, ip);
  Serial.begin(9600);
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, port)) {
    Serial.println("connected.");
    //print text to the server
    client.println("This is a request from the client.");
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

void loop()
{
  // if there are incoming bytes available 
  // from the server, read them and print them:
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();

    // do nothing forevermore:
    while(true);
  }
}
