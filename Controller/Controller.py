import pygame
pygame.init()

# white = (255,255,255)
# black = (0,0,0)
# gameWidth = 800
# gameHeight = 600
# squareSize = 20

# gameDisplay = pygame.display.set_mode((gameWidth,gameHeight))
# pygame.display.set_caption('CONTROL')

# pygame.display.update()

gameExit = False

# lead_x = gameWidth/2
# lead_y = gameHeight/2

deadzone = 0.04
sync1 = 1
sync2 = 2
sync3 = 3
driveChar = 0
turnChar = 0
digital1 = 4
digital2 = 5

joysticks = []
clock = pygame.time.Clock()

buttonString = "Temp"

f = open("Path.txt", "w")

for i in range(0, pygame.joystick.get_count()):
  joysticks.append(pygame.joystick.Joystick(i))
  joysticks[-1].init()
  print("Detected Controller:")
  print(joysticks[-1].get_name())

while not gameExit:
  clock.tick(600)

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

  # if event.type == pygame.JOYBUTTONDOWN: # D-Pad
  #   if event.button == 0:
  #     lead_y = lead_y - 5
  #   if event.button == 2:
  #     lead_x = lead_x - 5
  #   if event.button == 3:
  #     lead_x = lead_x + 5
  #   if event.button == 1:
  #     lead_y = lead_y + 5
  # if event.type == pygame.JOYAXISMOTION:
  #   if event.axis == 0:
  #     lead_x = lead_x + event.value
  #   if event.axis == 1:
  #     lead_y = lead_y + event.value

    # if event.type == pygame.JOYAXISMOTION:
    #   if (event.value < deadzone) & (event.value > -1*deadzone):
    #     value = 0;
    #   else:
    #     value = int(127 * event.value)
    #   if event.axis == 0:
    #     turnChar = value
    #     print("Turn = ")
    #     # lead_x = (event.value + 1) * (gameWidth / 2)
    #   if event.axis == 1:
    #     driveChar = value = value * -1
    #     print("Drive = ")
    #     # lead_y = (event.value + 1) * (gameHeight / 2)
    #   print(value)

      # if lead_y < 0:
      #   lead_y = 0
      # elif lead_y > gameHeight - squareSize:
      #   lead_y = gameHeight - squareSize
      # elif lead_x < 0:
      #   lead_x = 0
      # elif lead_x > gameWidth - squareSize:
      #   lead_x = gameWidth - squareSize

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

      # axis1 = joysticks.get_axis(0)
      # axis2 = joysticks.get_axis(1)
      # print("(", axis1, ", ", axis2, ")")

      # for i in range(0, pygame.joystick.get_count()):
      #   axis1 = joysticks.get_axis(i)
      #   axis2 = joysticks.get_axis(i+1)
      #   print("(", axis1, ", ", axis2, ")")
      #   i=i+1

    # gameDisplay.fill(black)
    # pygame.draw.rect(gameDisplay, white, [lead_x, lead_y, squareSize, squareSize])
    # pygame.display.update()
    f.write(str(sync1) + " " + str(sync2) + " " + str(sync3) + " " + str(driveChar) + " " + str(turnChar) + " " + str(digital1) + " " + str(digital2) + "\n")

f.write("\n\n\n")
f.close()

pygame.quit()

quit()
