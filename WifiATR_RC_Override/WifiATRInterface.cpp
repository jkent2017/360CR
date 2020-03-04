#include <Arduino.h>
#include "WifiATRInterface.h"

//-- public methods --//

//<<constructor>>
WifiATRInterface::WifiATRInterface(byte _mac[6], byte _robotIP[4], int _port, byte _gateway[4])
	//:ip(_robotIP), gateway(_gateway), subnet(255, 255, 255, 255), server(6060)
{
	index = 0; packetLength = sizeof(rxPacket);
	packet_rcvd = false;

	txPacket.pre1 = 0x53; txPacket.pre2 = 0x44; txPacket.pre3 = 0x52; txPacket.pre4 = 0x31;	//SDR1
	txPacket.post1 = 0x45; txPacket.post2 = 0x4F; txPacket.post3 = 0x46;					//EOF

	for (int i = 0; i < 5; i++) { mac[i] = _mac[i]; }
	port = _port;

	ip = new IPAddress(_robotIP);
	server = new EthernetServer(port);
}

//<<destructor>>
WifiATRInterface::~WifiATRInterface() { }

// new and delete operators
//void* operator new(size_t size){ return malloc(size); }
//void operator delete(void* ptr) { free(ptr); }

void WifiATRInterface::startEthernetServer()
{
	Ethernet.begin(mac, *ip);
	server->begin();
}

// Read available bytes, check if complete packet was received, and send response
bool WifiATRInterface::checkForPacket()
{
	// Read ethernet inputs
	EthernetClient client = server->available();
	readEthernet(client);
	if (packet_rcvd) {
		processPacket();
		//debugPrintRxPacket();

		// send response to PC
		packet_rcvd = false;

		// Send dummy return packet
		txPacket.digital = 0;
		//txPacket.analog1 = 12; txPacket.analog2 = 23; txPacket.analog3 = 34;

		memcpy(inputBuffer, &txPacket, sizeof(txPacket));
		server->write(inputBuffer, sizeof(txPacket));

		return true;
	}
	return false;
}

void WifiATRInterface::updateAnalogs(unsigned char an1, unsigned char an2, unsigned char an3)
{
	txPacket.analog1 = an1; //txPacket.analog2 = an2; txPacket.analog3 = an3;
}

//-- private methods --//
void WifiATRInterface::readEthernet(EthernetClient client)
{
	int bytesAvailable = client.available();
	// read packet
	if (bytesAvailable < packetLength) { return; }
	//Serial.print("Received "); Serial.print(bytesAvailable); Serial.println(" bytes");
	for (int i = 0; i < bytesAvailable; i++)
	{
		unsigned char readVal = client.read();
		//Serial.print(index); Serial.print(" "); Serial.println(readVal);
		if ((index == 0) && (readVal == 'S') && !packet_rcvd) {
			inputBuffer[index] = readVal;
			index = 1;
		}
		else if (index != 0) {
			inputBuffer[index] = readVal; index++;
			//Serial.println(readVal);
			if (index == 3) {  //header is 'SDR'
				if (inputBuffer[0] != 'S' || inputBuffer[1] != 'D' || inputBuffer[2] != 'R') {
					index = 0;  //bad header or out of sync: reset index
				}
			}
			if (index >= packetLength) {
				index = 0;
				packet_rcvd = true;
			}
		}
	}

	if (index >= sizeof(inputBuffer)) { index = 0; }  //memory leak protection
}

// Currently only works with up to 50 byte packets
void WifiATRInterface::processPacket()
{
	unsigned char tempPacket[50];
	memcpy(&tempPacket, inputBuffer, packetLength);  //copy buffer into tempPacket
	if (validateChecksum(tempPacket)) {
		memcpy(&rxPacket, tempPacket, packetLength);  //copy buffer into rxPacket
	}

}

bool WifiATRInterface::validateChecksum(unsigned char* packet)
{
	unsigned int calc = 0, checksum = packet[packetLength - 2] << 8 | packet[packetLength - 1];
	// print received packet
	//for(int i=0; i<packetLength; i++) { Serial.print(packet[i]); Serial.print(" "); }

	for (int i = 3; i < packetLength - 2; i++) {
		calc += packet[i];
	}

	//Serial.print("Checksums: "); Serial.print(calc);
	//Serial.print(" "); Serial.println(checksum);

	return (calc == checksum);
}