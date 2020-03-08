import pygame
import time
import serial

serialPort = '/dev/cu.usbmodem142201'
ser = serial.Serial(serialPort, 9600)

pygame.init()

gameExit = False
deadzone = 0.04
sync1 = 1
sync2 = 2
sync3 = 3
driveChar = 0
turnChar = 0
digital1 = 4
digital2 = 5
joysticks = []
buttonString = "Temp"

for i in range(0, pygame.joystick.get_count()):
  joysticks.append(pygame.joystick.Joystick(i))
  joysticks[-1].init()
  print("Detected Controller:")
  print(joysticks[-1].get_name())

while not gameExit:
  turnChar = joysticks[-1].get_axis(0)
  driveChar = joysticks[-1].get_axis(1)
  if (driveChar < deadzone) & (driveChar > -1*deadzone):
    driveChar = 0;
  else:
    driveChar = int(-127 * driveChar)

  if (turnChar < deadzone) & (turnChar > -1*deadzone):
    turnChar = 0;
  else:
    turnChar = int(127 * turnChar)

  for event in pygame.event.get():
    # print(event) # Debugging
    if event.type == pygame.QUIT:
      gameExit = True
    elif event.type == pygame.JOYBUTTONDOWN:
      if event.button == 0:
        buttonString = "D-Pad Up"
        pass # D-Up
      elif event.button == 1:
        buttonString = "D-Pad Down"
        pass # D-Down
      elif event.button == 2:
        buttonString = "D-Pad Left"
        pass # D-Left
      elif event.button == 3:
        buttonString = "D-Pad Right"
        pass # D-Right
      elif event.button == 4:
        buttonString = "Start"
        pass # Start
      elif event.button == 5:
        buttonString = "Select"
        pass # Select
      elif event.button == 6:
        buttonString = "Left Stick"
        pass # L-Stick Down
      elif event.button == 7:
        buttonString = "Right Stick"
        pass # R-Stick Down
      elif event.button == 8:
        buttonString = "LB"
        pass # LB
      elif event.button == 9:
        buttonString = "RB"
        pass # RB
      elif event.button == 10:
        gameExit = True
        buttonString = "Logitech"
        pass # Logitech
      elif event.button == 11:
        buttonString = "A"
        pass # A
      elif event.button == 12:
        buttonString = "B"
        pass # B
      elif event.button == 13:
        buttonString = "X"
        pass # X
      elif event.button == 14:
        buttonString = "Y"
        pass # Y
      print("Button Pressed: " + buttonString)
  ser.write(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2) + "\n")
  time.sleep(0.05)
ser.close()
pygame.quit()
quit()