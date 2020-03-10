import pygame
import time
import serial

serialPort = '/dev/cu.usbmodem143101'
ser = serial.Serial(serialPort, 9600)

pygame.init()

gameExit = False
deadzone = 0.04
sync1 = 1
sync2 = 2
sync3 = 3
driveChar = 0
turnChar = 0
digital1 = 1
digital2 = 5
maxSpeed = 5.0
joysticks = []
writing = False

for i in range(0, pygame.joystick.get_count()):
  joysticks.append(pygame.joystick.Joystick(i))
  joysticks[-1].init()
  print("Detected Controller:")
  print(joysticks[-1].get_name())

def checkButtons():
  global maxSpeed, gameExit, digital1, digital2, writing, f, reversePathFile
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
        f = open("Path.txt", "w")
        reversePathFile = open("Reverse.txt", "w")
        print("A")
      elif event.button == 12:
        writing = False
        f.close()
        reversePathFile.close()
        print("B")
      elif event.button == 13:
        readFile()
        print("X")
      elif event.button == 14:
      	reverseReverse();
        print("Y")

def readJoysticks():
  global turnChar, driveChar
  turnChar = joysticks[-1].get_axis(0)
  driveChar = joysticks[-1].get_axis(1)
  if (driveChar < deadzone) & (driveChar > -1*deadzone):
    driveChar = 0;
  else:
    driveChar = int(-127 * maxSpeed/5.0 * driveChar)

  if (turnChar < deadzone) & (turnChar > -1*deadzone):
    turnChar = 0;
  else:
    turnChar = int(127 * maxSpeed/5.0 * turnChar)

def readFile():
  global f, path
  print("Reading File")
  f = open("Path.txt", "r")
  path = f.readlines()
  for x in path:
    print(x)
    ser.write(x)
    time.sleep(0.05)
  f.close()
  print("Done Reading")

def reverseReverse():
  global reversePathFile, reversePath
  print("Reading File")
  reversePathFile = open("Reverse.txt", "r")
  reversePath = reversePathFile.readlines()
  for x in reversed(reversePath):
    print(x)
    ser.write(x)
    time.sleep(0.05)
  reversePathFile.close()
  print("Done Reading")


while not gameExit:
  
  readJoysticks()
  checkButtons()

  print(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2))
  print("Max Speed: " + str(maxSpeed) + "\n")

  ser.write(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2) + "\n")
  if writing:
    f.write(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2) + "\n")
    reversePathFile.write(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(-1*driveChar) + " " + str(-1*turnChar) + " " + str(digital1) + " " + str(digital2) + "\n")

  time.sleep(0.05)
f.close()
reversePathFile.close()
ser.close()
pygame.quit()
quit()