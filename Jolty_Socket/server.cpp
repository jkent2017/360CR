#include "server.h"

using namespace std;

server::server(){
	portnum = 8090;
	server(portnum);
}

server::server(int port) {
	drive = 127; turn = 127;
	client = socket(AF_INET, SOCK_STREAM, 0);
	if (client < 0) {
		cout << "\nERROR establishing socket...";
		exit(1);
	}

	cout << "\n--> Socket server created..\n";

	serv_addr.sin_port = htons(portnum);
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htons(INADDR_ANY);


	if (bind(client, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
		cout << "--> ERROR binding connection, the socket has already been established...\n";
		return -1;
	}

	size = sizeof(serv_addr);
	cout << "--> Looking for clients..." << endl;
	listen(client, 1);
	server = accept(client, (struct sockaddr*)&serv_addr, &size);
	if (server < 0)
        cout << "--> Error on connecting to client..." << endl;
    else {
        cout << "--> Connected to the client" << endl;
}

void listenForValues() {
    while (1) {
    	bzero(buffer, strlen(buffer));		// Clear buffer
        cout << "Client: ";					// Write to terminal
        recv(server, buffer, bufsize, 0);	// Recieve packet from Python
        // Set variables
        cout << buffer << endl;				// Write packet and insert newline
        if (check_exit(buffer))				// Check for "#"
            break;
    }
    cout << "\nDisconnected..." << endl;
}

bool check_exit(const char *msg) {
	for (int i = 0; i < strlen(msg); ++i) {
		if (msg[i] == '#') 
			return true;
	}
	return false;
}
