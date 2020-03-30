import pygame

from time import sleep

import serial.tools.list_ports
from gui import GUI, redraw, process_click, process_hover
from common import AXIS_LS_H, AXIS_LS_V, AXIS_LT, AXIS_RS_H, AXIS_RS_V, AXIS_RT

import socket
from serial import Serial
import os, re

class Comms():
  sock = None

  UDP_IP = ""
  UDP_PORT = 5555
  
  ser = None

  sync1 = 0
  sync2 = 0
  sync3 = 0
  digital1 = 1
  digital2 = 0

  def __init__(self):
    #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ports = [(port, desc) for port, desc, add in list(serial.tools.list_ports.comports())]
    if len(ports) > 0:
      self.ser = Serial(ports[0], 9600)

  def pack_message(self, drive, turn):
    #data = bytearray([0, 0, 0, turn, drive, 0])
    data = f'{self.sync1} {self.sync2} {self.sync3} {drive} {turn} {self.digital1} {self.digital2}'
    return data

  def send_message(self, drive, turn):
    drive = int(128 * drive) + 128
    turn  = int(128 * turn) + 128

    #self.sock.sendto(self.pack_message(id, drive, turn), (self.UDP_IP, self.UDP_PORT))
    if self.ser:
      self.ser.write(pack_message(drive, turn))

class Application():
  controller = None
  gui = None
  comms = None

  last_LS_pos = [-2, -2]
  last_RS_pos = [-2, -2]
  last_LT_pos = -2
  last_RT_pos = -2

  def __init__(self):
    self.gui = GUI()
    self.comms = Comms()
    self.init_joysticks()

  def init_joysticks(self):
    pygame.joystick.init()
    self.joysticks = []
    for i in range(pygame.joystick.get_count()):
      self.joysticks.append(pygame.joystick.Joystick(i))
      self.joysticks[-1].init()
      self.controller = self.joysticks[-1]
      print(f'Joystick {self.joysticks[-1].get_name()} initialized.')

  def on_button_pressed(self, button):
    self.gui.draw_button(button, True)

  def on_button_released(self, button):
    self.gui.draw_button(button, False)

  def on_joystick_hat(self, event):
    pass

  def get_left_trigger_pos(self, value):
    if abs(value - self.last_LT_pos) >= 0.01:
      self.last_LT_pos = value

  def get_right_trigger_pos(self, value):
    if abs(value - self.last_RT_pos) >= 0.01:
      self.last_RT_pos = value

  def get_left_stick_pos(self, vector):
    if abs(self.last_LS_pos[0] - vector[0]) >= 0.01 or abs(self.last_LS_pos[1] - vector[1]) >= 0.01:
      self.last_LS_pos = vector

  def get_right_stick_pos(self, vector):
    if abs(self.last_RS_pos[0] - vector[0]) >= 0.01 or abs(self.last_RS_pos[1] - vector[1]) >= 0.01:
      self.last_RS_pos = vector

  flag = False

  def check_controller(self):
    if not self.controller:
      self.flag = True
      print('No controller detected.')
      self.gui.draw_controller_disconnect()

    while not self.controller:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()

      self.init_joysticks() 

    if self.flag:
      self.flag = False
      redraw()

  def update_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        process_click(pygame.mouse.get_pos())
      elif event.type == pygame.JOYBUTTONDOWN:
        self.on_button_pressed(event.button)
      elif event.type == pygame.JOYBUTTONUP:
        self.on_button_released(event.button)
      elif event.type == pygame.JOYHATMOTION:
        self.on_joystick_hat(event)

    process_hover(pygame.mouse.get_pos())

    if self.controller:
      self.get_left_stick_pos([self.controller.get_axis(AXIS_LS_H), self.controller.get_axis(AXIS_LS_V)])
      self.get_right_stick_pos([self.controller.get_axis(AXIS_RS_H), self.controller.get_axis(AXIS_RS_V)])

      self.get_left_trigger_pos(self.controller.get_axis(AXIS_LT))
      self.get_right_trigger_pos(self.controller.get_axis(AXIS_RT))

  def update_graphics(self):
    # self.gui.panel_mapping.joystick_left.set_joystick_pos(self.last_LS_pos)
    # self.gui.panel_mapping.joystick_right.set_joystick_pos(self.last_RS_pos)
    self.gui.update()

  def update_comms(self):
    pass
    # self.comms.send_message(0, self.last_LS_pos[1], self.last_RS_pos[0])

  def run(self):
    clock = pygame.time.Clock()

    while True:
      # self.check_controller()
      self.update_events()
      self.update_graphics()
      self.update_comms()

      clock.tick(120)

if __name__ == "__main__":
  Application().run()