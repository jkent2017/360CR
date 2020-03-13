from socket import *
import time

address = ('192.168.1.177', 8888)

client_socket = socket(AF_INET, SOCK_DGRAM) #Set up the Socket
client_socket.settimeout(1) #Only wait 1 second for a response

while True:
  data = "Test"
  client_socket.sendto( data, address) #Send the data request
  print("Sent to Arduino")
  time.sleep(0.5)