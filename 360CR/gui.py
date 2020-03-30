# class MappingPanel(Panel):
#   button_a = None
#   button_b = None
#   button_x = None
#   button_y = None

#   joystick_left = None
#   joystick_right = None

#   def __init__(self, x, y, width, height, label, parent=None):
#     super().__init__(x, y, width, height, label, parent=parent)

#   def register_buttons(self, button_a, button_b, button_x, button_y):
#     self.button_a = button_a
#     self.button_b = button_b
#     self.button_x = button_x
#     self.button_y = button_y

#   def register_joysticks(self, joystick_left, joystick_right):
#     self.joystick_left = joystick_left
#     self.joystick_right = joystick_right

# class ControllerButton(Transform):
#   def __init__(self, x, y, parent):
#     super().__init__(pygame.Rect(x, y, 10, 10), parent)
    
#     self.default_colors = (common.gray, common.white)
#     self.colors = self.default_colors

#     self.pressed = False

#   def draw(self):
#     color = self.colors[1] if self.pressed else self.colors[0]
#     pygame.draw.circle(common.screen, color, self.get_pos(), self.get_size()[0])

#     Transform.draw(self)

#   def set_pressed(self, pressed):
#     self.pressed = pressed
#     self.draw()

# class ControllerJoystick(Transform):
#   joystick_pos = (-50, -50)

#   def __init__(self, x, y, parent):
#     super().__init__(pygame.Rect(x, y, 0, 0), parent)

#     self.default_colors = (common.gray, common.white)
#     self.colors = self.default_colors

#   def draw(self):
#     pygame.draw.circle(common.screen, common.dark_gray, self.get_pos(), 40)
#     pygame.draw.circle(common.screen, self.colors[0], self.get_pos(), 30)
#     pygame.draw.circle(common.screen, self.colors[1], self.joystick_pos, 10)

#   def set_joystick_pos(self, pos):
#     self.joystick_pos = (int(self.get_pos()[0] + pos[0] * 21), int(self.get_pos()[1] + pos[1] * 21))
#     self.draw()

# class GUI():
#   transforms = []

#   panel_message = None
#   panel_mapping = None
#   panel_setting = None
#   panel_camera  = None

#   def __init__(self):
#     pygame.font.init()

#     common.screen = pygame.display.set_mode((common.width, common.height))
#     common.font_18 = pygame.font.Font('fonts/karla.ttf', 18)
#     common.font_16 = pygame.font.Font('fonts/karla.ttf', 16)
#     common.font_12 = pygame.font.Font('fonts/karla.ttf', 12)
#     common.font_mono = pygame.font.Font('fonts/courierprimecode.ttf', 18)
#     pygame.display.set_caption('360 Camera Robot Application')

#     common.screen.fill(common.black)

#     # Panels
#     self.panel_message = MessagePanel(common.panel_message_x + common.spacing_lg, common.panel_message_y + common.spacing_lg, common.panel_message_width - common.spacing_lg * 2, common.panel_message_height - common.spacing_lg * 2, common.panel_message_label)
#     self.panel_mapping = MappingPanel(common.panel_mapping_x + common.spacing_lg, common.panel_mapping_y + common.spacing_lg, common.panel_mapping_width - common.spacing_lg * 2, common.panel_mapping_height - common.spacing_lg * 2, common.panel_mapping_label)
#     self.panel_setting = SettingPanel(common.panel_setting_x + common.spacing_lg, common.panel_setting_y + common.spacing_lg, common.panel_setting_width - common.spacing_lg * 2, common.panel_setting_height - common.spacing_lg * 2, common.panel_setting_label)
#     self.panel_camera  = CameraPanel(common.panel_camera_x + common.spacing_lg, common.panel_camera_y + common.spacing_lg, common.panel_camera_width - common.spacing_lg * 2, common.panel_camera_height - common.spacing_lg * 2, common.panel_camera_label)

#     self.add_object(self.panel_message)
#     self.add_object(self.panel_mapping)
#     self.add_object(self.panel_setting)
#     self.add_object(self.panel_camera)

#     # Message panel control buttons
#     self.add_object(ClearMessageButton('CLEAR', self.panel_message, self.panel_message.clear_messages))

#     button_center = 130
#     button_center_y = common.panel_mapping_height // 2 - 10 // 2
#     button_a = ControllerButton(button_center,      button_center_y + 20, self.panel_mapping)
#     button_b = ControllerButton(button_center + 20, button_center_y,      self.panel_mapping)
#     button_x = ControllerButton(button_center - 20, button_center_y,      self.panel_mapping)
#     button_y = ControllerButton(button_center,      button_center_y - 20, self.panel_mapping)

#     joystick_left = ControllerJoystick(50, button_center_y, self.panel_mapping)
#     joystick_right = ControllerJoystick(210, button_center_y, self.panel_mapping)

#     self.panel_mapping.register_buttons(button_a, button_b, button_x, button_y)
#     self.panel_mapping.register_joysticks(joystick_left, joystick_right)

#     # Mapping controller buttons
#     self.add_object(button_a)
#     self.add_object(button_b)
#     self.add_object(button_x)
#     self.add_object(button_y)
#     self.add_object(joystick_left)
#     self.add_object(joystick_right)

#     pygame.display.update()

#   def process_buttons(self):
#     pass

#   def process_joysticks(self):
#     pass

#   def draw_controller_disconnect(self):
#     common.screen.fill(common.black)

#     label  = 'No controller detected.'
#     label2 = 'Please connected to a supported controller.'
#     s  = common.font_18.size(label)
#     s2 = common.font_18.size(label2)

#     write(label, common.width // 2 - s[0] // 2, common.height // 2 - s[1] * 2, common.white, common.black, 18)
#     write(label2, common.width // 2 - s2[0] // 2, common.height // 2 - s2[1], common.white, common.black, 18)

#     pygame.display.update()

import pygame
import common

from common import BUTTON_A, BUTTON_B, BUTTON_X, BUTTON_Y
from common import panel_message_x, panel_message_y, panel_message_width, panel_message_height, panel_message_label
from common import panel_camera_x, panel_camera_y, panel_camera_width, panel_camera_height, panel_camera_label
from common import panel_control_x, panel_control_y, panel_control_width, panel_control_height, panel_control_label
from common import panel_mapping_width, panel_mapping_height, panel_mapping_label
from common import spacing_lg

from graphics import Transform, Panel, Button, Clickable, Hoverable, write

_transforms = {0 : []}
_current_depth = 0
_last_depth = 0

_popup_depth = 10

_panel_camera = None
_panel_control = None
_panel_message = None

def redraw():
  common.screen.fill(common.black)
  for transform in _transforms[_current_depth]:
    if not transform.parent:
      transform.draw()

def _add_object(obj):
  if _current_depth not in _transforms:
    _transforms[_current_depth] = []

  _transforms[_current_depth].append(obj) # add at parent's depth (cant rn because children are added first)
  obj.draw()

  return obj

def _remove_object(obj):
  if obj in _transforms[_current_depth]:
    for child in obj.children:
      _remove_object(child)

    _transforms[_current_depth].remove(obj)

    if obj.parent:
      obj.parent.children.remove(obj)

def _set_depth(depth):
  global _current_depth
  if depth != _current_depth:
    for transform in _transforms[_current_depth]:
      transform.set_enabled(False)

    _current_depth = depth
  
    if _current_depth not in _transforms:
      _transforms[_current_depth] = []
    else:
      for transform in _transforms[_current_depth]:
        transform.set_enabled(True)

def process_click(pos):
  for obj in _transforms[_current_depth]:
    if obj.enabled and isinstance(obj, Clickable) and obj.get_bounds().collidepoint(pos):
      obj.click()

def process_hover(pos):
  for obj in _transforms[_current_depth]:
    if obj.enabled and isinstance(obj, Hoverable):
      if obj.get_bounds().collidepoint(pos):
        obj.mouse_enter()
      else:
        obj.mouse_exit()

def create_options(on_close):
  _last_depth = _current_depth
  _set_depth(_popup_depth)

  _add_object(GUI._Popup(panel_mapping_width, panel_mapping_height, panel_mapping_label, on_close))

def Log(message):
  if _panel_message:
    _panel_message.add_message(message)

class GUI():
  class _MessagePanel(Panel):
    max_character_count_per_line = 100
    max_message_count = 6
    message_offset = 0
    messages = []

    def __init__(self, x, y, width, height, label, parent=None):
      super().__init__(x, y, width, height, label, parent=parent)
      _add_object(GUI._MessagePanel._ClearMessageButton('CLEAR', self, self.clear_messages))

    def draw(self):
      super().draw()
      self.draw_messages()

    def draw_messages(self):
      pygame.draw.rect(common.screen, common.dark_gray, self.get_bounds().inflate(-common.spacing_lg, -common.spacing_lg))
      for i in range(self.max_message_count):
        if self.message_offset + i >= len(self.messages):
          break
        self.draw_message(self.messages[self.message_offset + i], i)

    def draw_message(self, text, count):
      text_size = 16
      x = common.panel_message_x + common.spacing_lg * 2
      y = common.panel_message_y + common.spacing_lg * 2 + (text_size + common.spacing_lg) * count
      write(text, x, y, common.white, common.dark_gray, common.font_16)

    def add_message(self, text):
      text = text.strip()
      l = len(text)
      i = 0
      while l >= self.max_character_count_per_line:
        line = text[:self.max_character_count_per_line]
        line = line.strip()
        if i > 0:
          self.messages.append("  " + line)
        else:
          self.messages.append(line)
        text = text[self.max_character_count_per_line:]
        l -= self.max_character_count_per_line
        i += 1

      if l > 0:
        text = text.strip()
        self.messages.append("  " + text)

      if len(self.messages) >= self.max_message_count:
        self.message_offset = len(self.messages) - self.max_message_count

      self.draw_messages()

    def clear_messages(self):
      pygame.draw.rect(common.screen, common.dark_gray, self.get_bounds().inflate(-common.spacing_lg, -common.spacing_lg))
      self.messages.clear()
      self.message_offset = 0

    def scroll_messages_up(self):
      if self.message_offset > 0:
        self.message_offset -= 1
        self.draw()

    def scroll_messages_down(self):
      if self.message_offset < len(self.messages) - self.max_message_count:
        self.message_offset += 1
        self.draw()

    class _ClearMessageButton(Button):
      def __init__(self, label, parent, action):
        super().__init__(0, 0, 0, 0, label, parent, common.font_12)

        x = self.parent.get_size()[0] - self.get_size()[0]
        y = self.get_local_pos()[1] - self.get_size()[1]
        self.set_local_pos(x, y)

        self.action = action
        self.default_colors = (common.dark_gray, common.white)
        self.hover_colors = (common.dark_gray, common.blue)
        self.colors = self.default_colors

      def on_click(self):
        self.action()

      def draw(self):
        s = self.font.size(self.label)
        write(self.label, self.get_bounds().x + self.get_size()[0] // 2 - s[0] // 2, self.get_bounds().y + self.get_size()[1] // 2 - s[1] // 2, self.colors[1], common.black, self.font)

  class _CameraPanel(Panel):
    def __init__(self, x, y, width, height, label, parent=None):
      super().__init__(x, y, width, height, label, parent=parent)

  class _ControlPanel(Panel):
    def __init__(self, x, y, width, height, label, parent=None):
      super().__init__(x, y, width, height, label, parent=parent)

  class _Popup(Panel):
    def __init__(self, width, height, label, on_close):
      super().__init__(common.width // 2 - width // 2, common.height // 2 - height // 2, width, height, label, None)

      self.popup_return = None
      self.on_close = on_close

      _add_object(GUI._Popup._ClosePopupButton(self))

    class _ClosePopupButton(Button):
      def __init__(self, parent):
        super().__init__(0, 0, 0, 0, 'CLOSE', parent, common.font_12)

        x = self.parent.get_size()[0] - self.get_size()[0]
        y = self.get_local_pos()[1] - self.get_size()[1]
        self.set_local_pos(x, y)

        self.default_colors = (common.black, common.white)
        self.hover_colors = (common.black, common.blue)
        self.colors = self.default_colors

      def on_click(self):
        _remove_object(self.parent)
        _set_depth(_last_depth)
        redraw()

        if self.parent.on_close:
          self.parent.on_close()

      def draw(self):
        s = self.font.size(self.label)
        write(self.label, self.get_bounds().x + self.get_size()[0] // 2 - s[0] // 2, self.get_bounds().y + self.get_size()[1] // 2 - s[1] // 2, self.colors[1], self.colors[0], self.font)

  def __init__(self):
    pygame.font.init()
    common.screen = pygame.display.set_mode((common.width, common.height))
    common.font_18 = pygame.font.Font('fonts/karla.ttf', 18)
    common.font_16 = pygame.font.Font('fonts/karla.ttf', 16)
    common.font_14 = pygame.font.Font('fonts/karla.ttf', 14)
    common.font_12 = pygame.font.Font('fonts/karla.ttf', 12)
    common.font_mono = pygame.font.Font('fonts/courierprimecode.ttf', 18)
    pygame.display.set_caption('360CR User Application')

    common.screen.fill(common.black)

    _panel_message = GUI._MessagePanel(panel_message_x + spacing_lg, panel_message_y + spacing_lg, panel_message_width - spacing_lg * 2, panel_message_height - spacing_lg * 2, panel_message_label)
    _panel_camera = GUI._CameraPanel(panel_camera_x + spacing_lg, panel_camera_y + spacing_lg, panel_camera_width - spacing_lg * 2, panel_camera_height - spacing_lg * 2, panel_camera_label)
    _panel_control = GUI._ControlPanel(panel_control_x + spacing_lg, panel_control_y + spacing_lg, panel_control_width - spacing_lg * 2, panel_control_height - spacing_lg * 2, panel_control_label)

    _add_object(_panel_message)
    _add_object(_panel_camera)
    _add_object(_panel_control)

    pygame.display.update()

  def update(self):
    pygame.display.update()

  def draw_controller_disconnect(self):
    pass

  def draw_button(self, button, pressed):
    pass