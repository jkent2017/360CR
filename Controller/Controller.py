import pygame
import time
import socket

host = '192.168.1.177' # IP of Arduino
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
pygame.init()

gameExit = False
deadzone = 0.04
sync1 = 1
sync2 = 2
sync3 = 3
drive = 0
turn = 0
digital1 = 1
digital2 = 5
maxSpeed = 5.0
joysticks = []
writing = False
sleepTimer = 0.05
pathFile = open("Path.txt")
pathFile.close()
reversePathFile = open("Reverse.txt")
reversePathFile.close()

for i in range(0, pygame.joystick.get_count()):
  joysticks.append(pygame.joystick.Joystick(i))
  joysticks[-1].init()
  print("Detected Controller:")
  print(joysticks[-1].get_name())

def checkButtons():
  global maxSpeed, gameExit, digital1, digital2, writing, pathFile, reversePathFile
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameExit = True
    elif event.type == pygame.JOYBUTTONDOWN:
      print("Button Pressed: ")
      if event.button == 0:
        print("D-Pad Up")
        if maxSpeed < 5:
          maxSpeed = maxSpeed + 1
      elif event.button == 1:
        print("D-Pad Down")
        if maxSpeed > 1:
          maxSpeed = maxSpeed - 1
      elif event.button == 2:
        print("D-Pad Left")
      elif event.button == 3:
        print("D-Pad Right")
      elif event.button == 4:
        print("Start")
        digital1 = 0
      elif event.button == 5:
        print("Select")
        digital1 = 1
      elif event.button == 6:
        print("Left Stick")
      elif event.button == 7:
        print("Right Stick")
      elif event.button == 8:
        print("LB")
      elif event.button == 9:
        print("RB")
      elif event.button == 10:
        digital1 = 1
        gameExit = True
        print("Logitech")
      elif event.button == 11:
        writing = True
        pathFile = open("Path.txt", "w")
        reversePathFile = open("Reverse.txt", "w")
        print("A")
      elif event.button == 12:
        writing = False
        pathFile.close()
        reversePathFile.close()
        print("B")
      elif event.button == 13:
        readFile()
        print("X")
      elif event.button == 14:
        reverseReverse();
        print("Y")

def readJoysticks():
  global turn, drive
  turn = joysticks[-1].get_axis(0)
  drive = joysticks[-1].get_axis(1)
  if (drive < deadzone) & (drive > -1*deadzone):
    drive = 0;
  else:
    drive = int(-127 * maxSpeed/5.0 * drive)

  if (turn < deadzone) & (turn > -1*deadzone):
    turn = 0;
  else:
    turn = int(127 * maxSpeed/5.0 * turn)

def readFile():
  global pathFile, path, sleepTimer
  print("Reading File")
  pathFile = open("Path.txt", "r")
  path = pathFile.readlines()
  for x in path:
    print(x)
    s.send(str.encode(x))
    time.sleep(sleepTimer)
  pathFile.close()
  print("Done Reading")

def reverseReverse():
  global reversePathFile, reversePath, sleepTimer
  print("Reading File")
  reversePathFile = open("Reverse.txt", "r")
  reversePath = reversePathFile.readlines()
  for x in reversed(reversePath):
    print(x)
    s.send(str.encode(x))
    time.sleep(sleepTimer)
  reversePathFile.close()
  print("Done Reading")

while not gameExit:  
  readJoysticks()
  checkButtons()
  data = f'{sync1} {sync2} {sync3} {drive} {turn} {digital1} {digital2}\n' # Formatted String
  s.send(str.encode(data))
  print(data)
  print("Max Speed: " + str(maxSpeed) + "\n")
  if writing:
    pathFile.write(data)
    reversePathFile.write(data)
  time.sleep(sleepTimer)
pathFile.close()
reversePathFile.close()
pygame.quit()
quit()