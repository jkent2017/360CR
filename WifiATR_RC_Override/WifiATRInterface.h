#ifndef WIFIATR_H
#define WIFIATR_H

#include <Arduino.h>
//#include "SPI\SPI.h"
//#include <Ethernet2\src\Ethernet2.h>
#include <SPI.h>
#include <Ethernet2.h>
#include <stdlib.h>
#include "UtilityFunctions.h"	//new and delete functions

//class used to take serial packets with the WifiATR structure
class WifiATRInterface {
	public:
		WifiATRInterface(byte _mac[6], byte _robotIP[4], int _port, byte _gateway[4]);
		~WifiATRInterface();
		void startEthernetServer();
		bool checkForPacket();
		void updateAnalogs(unsigned char an1, unsigned char an2, unsigned char an3);

		// new and delete functions
		//void* operator new(size_t size);
		//void operator delete(void* ptr);

		// Received Packet
		struct {
			unsigned char sync_1;          // Header 'S'
			unsigned char sync_2;          // Header 'D'
			unsigned char sync_3;          // Header 'R'
			unsigned char driveChar = 127;
			unsigned char turnChar = 127;
			unsigned char digital_1 = 0;
			unsigned char digital_2 = 0;
		} rxPacket;

		/*	digital 1 bits
		*	0 - start path following
		*/	

		// Transmitted Packet
		struct
		{
			unsigned char pre1;
			unsigned char pre2;
			unsigned char pre3;
			unsigned char pre4;
			unsigned char digital;
			unsigned char analog1;
			unsigned char post1;
			unsigned char post2;
			unsigned char post3;
		} txPacket;

	private:
		// Packet parsing
		unsigned char inputBuffer[50];
		int index, packetLength;
		bool packet_rcvd;

		IPAddress* ip, gateway, subnet;
		EthernetServer* server;
		int port;
		
		byte mac[6];

		void readEthernet(EthernetClient client);
		void processPacket();
		bool validateChecksum(unsigned char* packet);
};
#endif
