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
    driveChar = int(-127 * maxSpeed/5.0 * driveChar)

  if (turnChar < deadzone) & (turnChar > -1*deadzone):
    turnChar = 0;
  else:
    turnChar = int(127 * maxSpeed/5.0 * turnChar)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameExit = True
    elif event.type == pygame.JOYBUTTONDOWN:
      if event.button == 0:
        buttonString = "D-Pad Up"
        if maxSpeed < 5:
        	maxSpeed = maxSpeed + 1
        pass # D-Up
      elif event.button == 1:
        buttonString = "D-Pad Down"
        if maxSpeed > 1:
        	maxSpeed = maxSpeed - 1
        pass # D-Down
      elif event.button == 2:
        buttonString = "D-Pad Left"
        pass # D-Left
      elif event.button == 3:
        buttonString = "D-Pad Right"
        pass # D-Right
      elif event.button == 4:
        buttonString = "Start"
        digital1 = 0
        pass # Start
      elif event.button == 5:
        buttonString = "Select"
        digital1 = 1
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
        digital1 = 1
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
  print(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2))
  print("Max Speed: " + str(maxSpeed) + "\n")
  time.sleep(0.05)
ser.close()
pygame.quit()
quit()