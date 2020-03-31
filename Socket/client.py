import socket	#for sockets
import sys	#for exit

host = '192.168.1.177' # IP of Arduino
port = 8888

# Create TCP Socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
except socket.error:
	print ('Failed to create socket')
	sys.exit()

sync1 = 1
sync2 = 2
sync3 = 3
drive = 0
turn = 0
digital1 = 1
digital2 = 5

while(1) :
	msg = input() # Wait until user presses enter to send data
	data = f'{sync1} {sync2} {sync3} {drive} {turn} {digital1} {digital2}\n' # Formatted String
	data = str.encode(data) # Encode to "bytes-like object"
	s.send(data) # Send data