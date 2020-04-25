import gui

from threading import Thread, Lock
from queue import Queue
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM, timeout

send_queue = None
connected = False

sock = None
server_addr = ('192.168.1.177', 8888)

digital2 = 1

writing = False

path_file = None
reverse_path_file = None

index = 0

last_send_mode = ''

path_list = []
reverse_list = []

def set_writing(enabled):
  global writing

  writing = enabled

def set_index(value):
  global index

  index = value

def open_path_reverse(rw):
  global reverse_path_file, reverse_list

  if rw == 'w':
    reverse_list = []

  reverse_path_file = open('Reverse.txt', rw)

def open_path(rw):
  global path_file

  if rw == 'w':
    path_list = []

  path_file = open('Path.txt', rw)

def close_path():
  if path_file:
    path_file.close()

def close_path_reverse():
  if reverse_path_file:
    reverse_path_file.close()

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
  
  def update(self, send_mode, drive, turn, max_speed, stop):
    global index, last_send_mode, send_queue, reverse_list, path_list, path_file, reverse_path_file

    if last_send_mode != send_mode:
      last_send_mode = send_mode
      send_queue = Queue()
      print(f'queue empty {send_queue.empty()}')

    drive = int(-127 * max_speed/5.0 * drive)
    turn = int(127 * max_speed/5.0 * turn)

    data = ''
    if send_mode == 'live':
      data = f'1 2 3 {drive} {turn} {stop} {digital2}\n'
    elif send_mode == 'path':
      if len(path_list) == 0:
        path_list = path_file.readlines()
      if len(path_list) > index:
        data = path_list[index]
        index += 1
    elif send_mode == 'reverse':
      if len(reverse_list) == 0:
        reverse_list = list(reversed(reverse_path_file.readlines()))
      if len(reverse_list) > index:
        data = reverse_list[index]
        index += 1

    send_queue.put(str.encode(data))
    
    if writing:
      path_file.write(data)
      reverse_path_file.write(data)
