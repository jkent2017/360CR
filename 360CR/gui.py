import pygame
import common
import communication

from graphics import Transform, Panel, Button, Clickable, Hoverable, Typeable, write

from threading import Thread

import cv2

comms = None

_transforms = []

_current_depth = 0
_last_depth = 0
_popup_depth = 10

_focused_obj = None
_popup_return_obj = None

_message_bar = None

_controller = None

_send_mode = 'live' # path, reverse


def redraw():
  common.screen.fill(common.color_bg_main)

  for obj in _transforms:
    obj.draw()

def _add_object(obj):
  if not obj.parent:
    _transforms.append(obj)
  
  redraw()

  return obj

def _remove_object(obj):
  if obj in _transforms:
    _transforms.remove(obj)
  else:
    for transform in _transforms:
      if obj in transform.children:
        transform.children.remove(obj)
        break
  
  redraw()

def _set_depth(depth):
  global _current_depth
  if depth != _current_depth:
    for transform in _transforms:
      if transform.depth == _current_depth:
        transform.set_enabled(False)

    _current_depth = depth
  
    for transform in _transforms:
      if transform.depth == _current_depth:
        transform.set_enabled(True)

def create_popup(width, height, label, on_close):
  _popup_return_obj = None

  _last_depth = _current_depth
  _set_depth(_popup_depth)

  _add_object(Popup(width, height, label, on_close))

def process_click(pos):
  global _focused_obj
  for obj in _transforms:
    if _process_click(pos, obj):
      break

def _process_click(pos, obj):
  global _focused_obj

  if obj.enabled:
    if len(obj.children) > 0:
      for child in obj.children:
        if _process_click(pos, child):
          return True

    if isinstance(obj, Clickable) and obj.get_bounds().collidepoint(pos):
      if isinstance(obj, Typeable):
        _focused_obj = obj
      else:
        _focused_obj = None

      obj.click()
      return True
    return False

def process_hover(pos):
  for obj in _transforms:
    _process_hover(pos, obj)

def _process_hover(pos, obj):
  if obj.enabled:
    if len(obj.children) > 0:
      for child in obj.children:
        _process_hover(pos, child)

    if isinstance(obj, Hoverable):
      if obj.get_bounds().collidepoint(pos):
        obj.mouse_enter()
      else:
        obj.mouse_exit()

def process_key_down(key):
  if _focused_obj:
    if (key.key >= 48 and key.key <= 57) or (key.key >= 97 and key.key <= 122) or (key.key >= 256 and key.key <= 265) or key.key == 32:
      if common.font_14.size(_focused_obj.text + key.unicode)[0] < _focused_obj.get_size()[0]:
        _focused_obj.add_char(key.unicode)
    elif key.key == 8:
      _focused_obj.del_char()
    else:
      print(f'key {key.unicode} / {key.key} not recognized')

    _focused_obj.draw()

def process_key_up(key):
  pass

def process_button_down(button):
  if button == common.BUTTON_SL:
    communication.digital1 = 1
  elif button == common.BUTTON_ST:
    communication.digital1 = 0

def process_button_up(button):
  pass

def Log(message):
  if _message_bar:
    _message_bar.add_message(message)
  print(message)

class _PairingTablePanel(Panel):
  def __init__(self):
    super().__init__(20, 95, common.width -40, common.height - 20 - 95, '')

  def draw(self):
    tab_width = 100
    tab_height = 20

    outer_top_left = (self.get_bounds().x, self.get_bounds().y + tab_height + 2)
    outer_top_right = (self.get_bounds().x + self.get_bounds().width - 1, self.get_bounds().y + tab_height + 2)
    outer_bottom_left = (self.get_bounds().x, self.get_bounds().y + self.get_bounds().height - 2)
    outer_bottom_right = (self.get_bounds().x + self.get_bounds().width - 1, self.get_bounds().y + self.get_bounds().height - 2)

    inner_top_left = (outer_top_left[0] + 2, outer_top_left[1] + 2)
    inner_top_right = (outer_top_right[0] - 2, outer_top_right[1] + 2)
    inner_bottom_left = (outer_bottom_left[0] + 2, outer_bottom_left[1] - 2)
    inner_bottom_right = (outer_bottom_right[0] - 2, outer_bottom_right[1] - 2)
    
    tab_start = (outer_top_left[0], outer_top_left[1])
    tab_end = (tab_start[0] + tab_width, tab_start[1])
    tab_start_top = (tab_start[0], tab_start[1] - tab_height)
    tab_end_top = (tab_end[0], tab_end[1] - tab_height)

    panel_rect = pygame.Rect(outer_top_left[0], outer_top_left[1], outer_top_right[0] - outer_top_left[0], outer_bottom_left[1] - outer_top_left[1])
    tab_rect = pygame.Rect(tab_start_top[0], tab_start_top[1], tab_end_top[0] - tab_start_top[0], tab_start[1] - tab_start_top[1])

    pygame.draw.rect(common.screen, common.color_bg_light, panel_rect)
    pygame.draw.rect(common.screen, common.color_bg_light, tab_rect)

    s = common.font_14.size('Pairing Table')
    write('Pairing Table', tab_rect.x + tab_rect.width // 2 - s[0] // 2, tab_rect.y + tab_rect.height // 2 - s[1] // 2, common.color_text_dark, common.color_bg_light, common.font_14)

    # outer gray box
    pygame.draw.line(common.screen, common.color_bg_dark, outer_top_left, tab_start, 1)

    # tab
    pygame.draw.line(common.screen, common.color_bg_dark, tab_start, (tab_start_top[0], tab_start_top[1] + 2), 1)
    pygame.draw.line(common.screen, common.color_accent_gold, (tab_start_top[0], tab_start_top[1] + 2), (tab_start_top[0] + 2, tab_start_top[1]), 1)
    pygame.draw.line(common.screen, common.color_accent_gold, (tab_start_top[0] + 2, tab_start_top[1]), (tab_end_top[0] - 2, tab_end_top[1]), 1)
    pygame.draw.line(common.screen, common.color_accent_gold, (tab_end_top[0] - 2, tab_end_top[1]), (tab_end_top[0], tab_end_top[1] + 2), 1)
    pygame.draw.line(common.screen, common.color_accent_yellow, (tab_start_top[0] + 2, tab_start_top[1] + 1), (tab_end_top[0] - 2, tab_end_top[1] + 1), 1)
    pygame.draw.line(common.screen, common.color_accent_yellow, (tab_start_top[0] + 1, tab_start_top[1] + 2), (tab_end_top[0] - 1, tab_end_top[1] + 2), 1)
    pygame.draw.line(common.screen, common.color_bg_dark, (tab_end_top[0], tab_end_top[1] + 3), tab_end, 1)

    # outer gray box continued
    pygame.draw.line(common.screen, common.color_bg_dark, tab_end, outer_top_right, 1)
    pygame.draw.line(common.screen, common.color_bg_dark, outer_top_left, outer_bottom_left, 1)
    pygame.draw.line(common.screen, common.color_bg_dark, outer_top_right, outer_bottom_right, 1)
    pygame.draw.line(common.screen, common.color_bg_dark, outer_bottom_left, outer_bottom_right, 1)

    # inner blue box
    pygame.draw.line(common.screen, common.color_accent_blue, inner_top_left, inner_top_right, 1)
    pygame.draw.line(common.screen, common.color_accent_blue, inner_top_left, inner_bottom_left, 1)
    pygame.draw.line(common.screen, common.color_accent_blue, inner_top_right, inner_bottom_right, 1)
    pygame.draw.line(common.screen, common.color_accent_blue, inner_bottom_left, inner_bottom_right, 1)

    # table header

    header_rect = pygame.Rect(inner_top_left[0] + 1, inner_top_left[1] + 1, inner_top_right[0] - inner_top_left[0] - 1, 20)
    header_name_rect = pygame.Rect(header_rect.x, header_rect.y + header_rect.height // 2 - 14 // 2, 250, 14)
    header_ip_rect = pygame.Rect(header_name_rect.x + header_name_rect.width + 12, header_name_rect.y, 250, 14)

    #pygame.draw.rect(common.screen, common.color_accent_yellow, header_rect)
    #pygame.draw.rect(common.screen, common.color_accent_blue, header_name_rect)
    #pygame.draw.rect(common.screen, common.color_accent_blue, header_ip_rect)

    s = common.font_14.size('Radio ID ?')
    write('Radio ID ?', header_name_rect.x + header_name_rect.width // 2 - s[0] // 2, header_name_rect.y + header_name_rect.height // 2 - s[1] // 2, common.color_text_dark, common.color_bg_light, common.font_14)
    s = common.font_14.size('IP Address ?')
    write('IP Address ?', header_ip_rect.x + header_ip_rect.width // 2 - s[0] // 2, header_ip_rect.y + header_ip_rect.height // 2 - s[1] // 2, common.color_text_dark, common.color_bg_light, common.font_14)

    # divider
    pygame.draw.line(common.screen, common.color_bg_dark,  (header_name_rect.x + header_name_rect.width + 5, inner_top_left[1] + 5), (header_name_rect.x + header_name_rect.width + 5, inner_top_left[1] + 15), 1)
    pygame.draw.line(common.screen, common.color_bg_light, (header_name_rect.x + header_name_rect.width + 6, inner_top_left[1] + 5), (header_name_rect.x + header_name_rect.width + 6, inner_top_left[1] + 15), 1)

    pygame.draw.line(common.screen, common.color_bg_dark,  (header_ip_rect.x + header_ip_rect.width + 5, inner_top_left[1] + 5), (header_ip_rect.x + header_ip_rect.width + 5, inner_top_left[1] + 15), 1)
    pygame.draw.line(common.screen, common.color_bg_light, (header_ip_rect.x + header_ip_rect.width + 6, inner_top_left[1] + 5), (header_ip_rect.x + header_ip_rect.width + 6, inner_top_left[1] + 15), 1)

class _MessageBar(Panel):

  max_character_count_per_line = 100
  current_message = 'Ready'

  def __init__(self):
    super().__init__(0, common.height - 20, common.width, 20, '')

  def draw(self):
    pygame.draw.rect(common.screen, common.color_bg_main, self.get_bounds())

    s = common.font_14.size(self.current_message)
    x = self.get_bounds().x + self.get_bounds().width - s[0] - 5
    y = self.get_bounds().y + self.get_bounds().height // 2 - s[1] // 2 - 2
    write(self.current_message, x, y, common.color_text_dark, common.color_bg_main, common.font_14)

  def add_message(self, text):
    text = text.strip()
    text = text[:self.max_character_count_per_line]

    self.current_message = text
    self.draw()

  def clear_messages(self):
    self.add_message('Ready')

class _ControlPanel(Panel):
  def __init__(self):
    super().__init__(0, 0, common.width, 75, '')

class PanelButton(Button):
  def __init__(self, x, y, width, height, label, parent=None, font=common.font_18, action=None):
    super().__init__(x, y, width, height, label, parent, font, action)

    self.default_colors = (common.color_bg_main, common.color_bg_main, common.color_text_dark)
    self.highlight_colors = ((216, 230, 242), common.color_accent_blue, common.color_text_dark)
    self.disabled_colors = (common.color_bg_main, common.color_bg_main, common.color_bg_dark)
    self.colors = self.default_colors

class Popup(Panel, Clickable):
  def __init__(self, width, height, label, on_close):
    super().__init__(0, 0, common.width, common.height, '', parent=None)

    self.on_close = on_close
    self.return_obj = None

    _add_object(Popup.PopupForeground(width, height, label, self))

  def on_click(self):
    _remove_object(self)
    _set_depth(_last_depth)

    if self.on_close:
      self.on_close(self.return_obj)

  def submit(self):
    #global _popup_return_obj
    #_popup_return_obj = 
    self.return_obj = self.children[0].children[0].text
    self.on_click()

  class PopupForeground(Panel, Clickable):
    def __init__(self, width, height, label, parent):
      super().__init__(common.width // 2 - width // 2, common.height // 2 - height // 2, width, height, '', parent)
      
      self.text_input = TextInput(width // 2 - 200 // 2, height // 2 - 25 // 2, 200, 25, parent=self)
      _add_object(self.text_input)

      self.submit_button = Button(0, 0, 0, 0, 'submit', self, common.font_14, self.parent.submit)
      self.submit_button.set_size(self.submit_button.get_size()[0] + 10, self.submit_button.get_size()[1] + 4)
      self.submit_button.set_local_pos(self.text_input.get_local_pos()[0] + self.text_input.get_size()[0] - self.submit_button.get_size()[0], self.text_input.get_local_pos()[1] + self.submit_button.get_size()[1] + 6)
      _add_object(self.submit_button)

      self.label = label

    def on_click(self):
      self.draw()

    def draw(self):
      r = pygame.Rect(self.get_bounds().x + 1, self.get_bounds().y + 1, self.get_bounds().width, self.get_bounds().height)

      pygame.draw.rect(common.screen, common.color_bg_dark, r)
      pygame.draw.rect(common.screen, common.color_bg_main, self.get_bounds())
      pygame.draw.rect(common.screen, common.color_bg_dark, self.get_bounds(), 1)

      s = common.font_16.size(self.label)
      write(self.label, self.text_input.get_pos()[0], self.text_input.get_pos()[1] - s[1] - 2, self.colors[2], self.colors[0], common.font_16)

      Transform.draw(self)

class TextInput(Transform, Clickable, Hoverable, Typeable):
  def __init__(self, x, y, width, height, parent=None, clear_on_click=False):
    Transform.__init__(self, pygame.Rect(x, y, width, height), parent)
    Hoverable.__init__(self)

    self.default_colors = (common.color_bg_light, common.color_bg_dark, common.color_text_dark)
    self.highlight_colors = (common.color_bg_light, common.color_accent_blue, common.color_text_dark)
    self.disabled_colors = (common.color_bg_mid_dark, common.color_bg_dark, common.color_text_dark)
    self.focused_colors = (common.color_bg_light, common.color_accent_gold, common.color_text_dark)

    self.colors = self.default_colors
    self.clear_on_click = clear_on_click

  def draw(self):
    if _focused_obj == self:
      self.colors = self.focused_colors
    elif self.is_hovered:
      self.colors = self.highlight_colors
    elif not self.enabled:
      self.colors = self.disabled_colors
    else:
      self.colors = self.default_colors

    pygame.draw.rect(common.screen, self.colors[0], self.get_bounds())
    pygame.draw.rect(common.screen, self.colors[1], self.get_bounds(), 1)
    
    s = common.font_14.size(self.text)
    write(self.text, self.get_pos()[0] + 5, self.get_pos()[1] + self.get_size()[1] // 2 - s[1] // 2, self.colors[2], self.colors[0], common.font_14)

    Transform.draw(self)

  def on_click(self):
    if self.clear_on_click:
      self.text = ''
    self.draw()

  def on_mouse_enter(self):
    self.colors = self.highlight_colors
    self.draw()

  def on_mouse_exit(self):
    self.colors = self.default_colors
    self.draw()

class RadioButton(Transform, Clickable, Hoverable):
  def __init__(self, x, y, index, parent):
    super().__init__(pygame.Rect(x, y, 14, 14), parent)
    self.index = index

    self.colors = ((243, 243, 239), common.color_bg_dark, common.color_text_dark)

  def draw(self):
    pygame.draw.rect(common.screen, self.colors[0], self.get_bounds())
    pygame.draw.rect(common.screen, self.colors[1], self.get_bounds(), 1)
    if self.parent.selected == self.index:
      r = pygame.Rect(self.get_bounds().x + 2, self.get_bounds().y + 2, self.get_bounds().width - 4, self.get_bounds().height - 4)
      pygame.draw.rect(common.screen, self.colors[1], r)

  def on_click(self):
    self.parent.select(self.index)
    self.parent.draw()

  def on_mouse_enter(self):
    self.colors = ((216, 230, 242), common.color_accent_blue, common.color_text_dark)
    self.draw()

  def on_mouse_exit(self):
    self.colors = ((243, 243, 239), common.color_bg_dark, common.color_text_dark)
    self.draw()

class RadioButtons(Transform):
  _buttons = []
  _labels = []
  _values = []
  selected = 0

  def __init__(self, x, y, title, labels, values, parent=None, on_select=None):
    super().__init__(pygame.Rect(x, y, 0, 0), parent)

    self.title = title
    self._labels = labels
    self._values = values
    self.on_select = on_select

    dx = common.font_16.size(title)[0] + 10
    dy = 2

    for i in range(len(self._labels)):
      s = common.font_14.size(self._labels[i])

      dx += s[0] + 2
      self._buttons.append(RadioButton(dx, dy, i, self))
      
      dx += 14 + 8

    self.set_size(dx, 35)

    if on_select:
      on_select(values[self.selected])

  def draw(self):
    x = self.get_pos()[0]
    y = self.get_pos()[1]

    t = common.font_16.size(self.title)
    write(self.title, x, y, common.color_text_dark, common.color_bg_main, common.font_16)

    x += t[0] + 10

    for i in range(len(self._labels)):
      s = common.font_14.size(self._labels[i])
      write(self._labels[i], x, y, common.color_text_dark, common.color_bg_main, common.font_14)
      x += s[0] + 2 + 14 + 8

    Transform.draw(self)
  
  def select(self, index):
    self.selected = index
    if self.on_select:
      self.on_select(self._values[self.selected])

class PathControls(Transform):
  def __init__(self, parent, cb_record, cb_stop, cb_follow):
    super().__init__(pygame.Rect(common.width - 148 - 126, 0, 126, parent.get_bounds().height - 10), parent)

    self.record_button = Button(8,  5, 110, 20, 'start recording', self, common.font_14, cb_record)
    self.stop_button   = Button(8, 27, 110, 20, 'stop recording', self, common.font_14, cb_stop)
    self.follow_button = Button(8, 49, 110, 20, 'follow path', self, common.font_14, cb_follow)

    self.record_button.set_enabled(True)
    self.stop_button.set_enabled(False)
    self.follow_button.set_enabled(False)

  def draw(self):
    x = self.get_pos()[0]
    pygame.draw.line(common.screen, common.color_bg_dark, (x, 10), (x, 65), 1)
    pygame.draw.line(common.screen, common.color_bg_light, (x+1, 10), (x+1, 65), 1)
    Transform.draw(self)

class OptionsPanel(Transform):
  def __init__(self, parent, cb_video, cb_controller, cb_connect):
    super().__init__(pygame.Rect(common.width - 148, 0, 148, parent.get_bounds().height - 10), parent)

    Button(8,  5, 132, 20, 'open video stream', self, common.font_14, cb_video)
    Button(8, 27, 132, 20, 'connect controller', self, common.font_14, cb_controller)
    Button(8, 49, 132, 20, 'connect to robot', self, common.font_14, cb_connect)

  def draw(self):
    x = self.get_pos()[0]
    pygame.draw.line(common.screen, common.color_bg_dark, (x, 10), (x, 65), 1)
    pygame.draw.line(common.screen, common.color_bg_light, (x+1, 10), (x+1, 65), 1)
    Transform.draw(self)

class SpeedControls(Transform):
  def __init__(self, parent, cb_change_speed):
    super().__init__(pygame.Rect(common.width - 148 - 126 - 126, 0, 126, parent.get_bounds().height - 10), parent)

    self.callback = cb_change_speed
    self.input = TextInput(8, 27, 110, 20, self, True)
    self.input.text = '0'

    Button(8, 49, 110, 20, 'submit', self, common.font_14, self.change_speed)

  def draw(self):
    s = common.font_14.size('max speed')
    write('max speed', self.get_pos()[0] + 126 // 2 - s[0] // 2, self.get_pos()[1] + 5 + 1, common.color_text_dark, common.color_bg_main, common.font_14)

    x = self.get_pos()[0]
    pygame.draw.line(common.screen, common.color_bg_dark, (x, 10), (x, 65), 1)
    pygame.draw.line(common.screen, common.color_bg_light, (x+1, 10), (x+1, 65), 1)
    Transform.draw(self)

  def change_speed(self):
    try:
      int(self.input.text)
    except:
      Log(f'{self.input.text} not a valid speed value')
      self.input.text = '1'
      self.draw()

    if int(self.input.text) < 0 or int(self.input.text) > 5:
      Log('Cant set speed that high, defaulting to 1')
      self.input.text = '1'
      self.draw()
    else:
      self.callback(int(self.input.text))

class GUI():
  control_panel_button_connect = None
  video_open = False

  last_LS_pos = [-2, -2]  
  last_RS_pos = [-2, -2]
  max_speed = 0

  def __init__(self):
    global _message_bar, comms

    pygame.font.init()
    common.screen = pygame.display.set_mode((common.width, common.height))
    pygame.display.set_caption('FlexCSR User Application')
    common.font_18 = pygame.font.Font('fonts/karla.ttf', 18)
    common.font_16 = pygame.font.Font('fonts/karla.ttf', 16)
    common.font_14 = pygame.font.Font('fonts/karla.ttf', 14)
    common.font_12 = pygame.font.Font('fonts/karla.ttf', 12)
    common.font_mono = pygame.font.Font('fonts/courierprimecode.ttf', 18)
    common.screen.fill(common.color_bg_main)

    _message_bar = _MessageBar()
    _add_object(_message_bar)

    self.connect_controller()

    comms = communication.Comms()

    control_panel = _ControlPanel()
    OptionsPanel(control_panel, self.open_stream, self.connect_controller, self.establish_connection)
    SpeedControls(control_panel, self.change_max_speed)
    self.path_controls = PathControls(control_panel, self.path_record, self.path_stop, self.path_follow)

    _add_object(control_panel)

    pygame.display.update()

  def open_stream(self):
    if self.video_open:
      Log('stream already open')
    else:
      Thread(target=self.thread_function, daemon=True).start()

  def thread_function(self):
    cap = cv2.VideoCapture('rtsp://root:360CameraRobot@192.168.1.57:554/live.sdp')

    if not cap.isOpened():
      Log('Error opening video')
    else:
      self.video_open = True
      #self.start_stream.set_enabled(False)

    while (cap.isOpened()):
      ret, frame = cap.read()
      if ret:
        cv2.imshow('Frame', frame)

        if cv2.waitKey(25) & 0xff == ord('q'):
          break

      else:
        break

    cap.release()
    cv2.destroyAllWindows()
    self.video_open = False
    #self.start_stream.set_enabled(True)

  def connect_controller(self):
    global _controller

    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
      _controller = pygame.joystick.Joystick(0)
      _controller.init()

      Log(f'{_controller.get_name()} initialized')
    else:
      Log(f'No controllers detected')

  def path_record(self):
    Log('Started recording path')
    communication.writing = True
    communication.path_file = open("Path.txt", "w")
    communication.reverse_path_file = open("Reverse.txt", "w")

    self.path_controls.record_button.set_enabled(False)
    self.path_controls.stop_button.set_enabled(True)
    self.path_controls.follow_button.set_enabled(False)

  def path_stop(self):
    global _send_mode

    Log('Stopped recording path')
    _send_mode = 'live'
    communication.writing = False
    communication.path_file.close()
    communication.reverse_path_file.close()
    communication.index = 0

    self.path_controls.record_button.set_enabled(True)
    self.path_controls.stop_button.set_enabled(False)
    self.path_controls.follow_button.set_enabled(True)

  def path_follow(self):
    global _send_mode

    communication.index = 0
    communication.writing = False
    communication.path_file = open("Path.txt", "r")

    _send_mode = 'path'

  def path_home(self):
    global _send_mode

    communication.index = 0
    communication.writing = False
    communication.reverse_path_file = open("Reverse.txt", "r")

    _send_mode = 'reverse'

  def change_max_speed(self, speed):    
    self.max_speed = speed
    Log(f'set max speed to {self.max_speed}')

  def establish_connection(self):
    comms.establish_connection()

  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        process_click(pygame.mouse.get_pos())
      elif event.type == pygame.KEYDOWN:
        process_key_down(event)
      elif event.type == pygame.KEYUP:
        process_key_up(event)
      elif event.type == pygame.JOYBUTTONDOWN:
        process_button_down(event.button)
      elif event.type == pygame.JOYBUTTONUP:
        process_button_up(event.button)
      elif event.type == pygame.JOYHATMOTION:
        pass

    process_hover(pygame.mouse.get_pos())

    if _controller:
      self.set_left_stick_pos([_controller.get_axis(common.AXIS_LS_H), _controller.get_axis(common.AXIS_LS_V)])
      self.set_right_stick_pos([_controller.get_axis(common.AXIS_RS_H), _controller.get_axis(common.AXIS_RS_V)])

    pygame.display.update()

  def set_left_stick_pos(self, vector):
    if abs(self.last_LS_pos[0] - vector[0]) >= 0.01 or abs(self.last_LS_pos[1] - vector[1]) >= 0.01:
      self.last_LS_pos = vector

  def set_right_stick_pos(self, vector):
    if abs(self.last_RS_pos[0] - vector[0]) >= 0.01 or abs(self.last_RS_pos[1] - vector[1]) >= 0.01:
      self.last_RS_pos = vector

  def run(self):
    clock = pygame.time.Clock()

    while True:
      self.update()
      comms.update(_send_mode, self.last_LS_pos[1], self.last_RS_pos[0], self.max_speed)
      clock.tick(120)