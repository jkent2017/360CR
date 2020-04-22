import gui

from threading import Thread, Lock
from queue import Queue
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM, timeout

send_queue = None
connected = False

sock = None
server_addr = ('192.168.1.177', 8888)

digital1 = 1
digital2 = 5

writing = False

path_file = None
reverse_path_file = None

index = 0

def thread_communicate():
  while sock:
    try:
      message = send_queue.get(True)
      sock.sendall(message)
      gui.Log(f'sending {message}')

    except:
      gui.Log('error raised')
      break

class Comms():
  def __init__(self):
    global send_queue
    send_queue = Queue()

    path_file = open("Path.txt")
    path_file.close()
    reverse_path_file = open("Reverse.txt")
    reverse_path_file.close()

  def establish_connection(self):
    global sock
    if sock:
      sock.close()
      sleep(1)
      sock = None

    sock = socket(AF_INET, SOCK_STREAM)
    try:
      gui.Log('trying to connect... may take up to 2 minutes')
      sock.connect(server_addr)
      gui.Log('connection with arduino successful')
      Thread(target=thread_communicate, daemon=True).start()
    except ConnectionRefusedError:
      gui.Log('connection refused')
      sock = None
    except timeout:
      gui.Log('socket timed out')
      sock = None
    except:
      gui.Log('exception raised on socket connect')
      sock = None
  
  def update(self, send_mode, drive, turn, max_speed):
    global index

    drive = int(-127 * max_speed/5.0 * drive)
    turn = int(127 * max_speed/5.0 * turn)

    data = ''
    if send_mode == 'live':
      data = f'1 2 3 {drive} {turn} {digital1} {digital2}\n'
    elif send_mode == 'path':
      if len(path_file.readlines()) > index:
        data = path_file.readlines()[index]
        index += 1
    elif send_mode == 'reverse':
      if len(reverse_path_file.readlines()) > index:
        data = reversed(reverse_path_file.readlines())[index]
        index += 1

    send_queue.put(str.encode(data))
    
    if writing:
      path_file.write(data)
      reverse_path_file.write(data)