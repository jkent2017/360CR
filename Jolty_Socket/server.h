#ifndef SERVER_H
#define SERVER_H

#include <Arduino.h>
#include <sys/socket.h>
#include <netinet/in.h>

class server{
public:
	server();
	server(port);
	void listenForValues();
	~server();

private:
	unsigned char drive, turn;
	bool check_exit(const char *msg);
	int portnum;
	int bufsize;
	int client, server;
	socklen_t size;
	struct sockaddr_in serv_addr;
	char buffer[bufsize]; 
};
#endif
