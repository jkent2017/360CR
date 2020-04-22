import pygame
import common

def write(text, x, y, color, bg, font):
  bitmap = font.render(text, True, color, bg)
  common.screen.blit(bitmap, (x,y))

class Transform():
  def __init__(self, rect, parent=None):
    self.bounds = rect
    self.parent = parent
    self.children = []

    self.default_colors = (common.color_bg_light, common.color_bg_dark, common.color_text_dark)
    self.colors = self.default_colors
    self.disabled_colors = (common.color_bg_mid_dark, common.color_bg_dark, common.color_bg_dark)

    self.enabled = True
    self.depth = 0

    if parent:
      parent.children.append(self)

  def draw(self):
    for child in self.children:
      child.draw()

  def set_enabled(self, enabled):
    self.enabled = enabled
    self.colors = self.default_colors if enabled else self.disabled_colors

    for child in self.children:
      child.set_enabled(enabled)

    self.draw()

  def set_depth(self, depth):
    self.depth = depth

  def set_local_pos(self, x, y):
    self.bounds.x = x
    self.bounds.y = y
    self.parent.draw() if self.parent else self.draw()

  def set_size(self, width, height):
    self.bounds.width = width
    self.bounds.height = height
    self.parent.draw() if self.parent else self.draw()

  def get_local_pos(self):
    return (self.bounds.x, self.bounds.y)

  def get_pos(self):
      return (self.parent.get_pos()[0] + self.bounds.x, self.parent.get_pos()[1] + self.bounds.y) if self.parent else (self.bounds.x, self.bounds.y)

  def get_size(self):
    return (self.bounds.width, self.bounds.height)

  def get_parent(self):
    return self.parent

  def get_bounds(self):
    return pygame.Rect(self.get_pos()[0], self.get_pos()[1], self.bounds.width, self.bounds.height)

class Clickable():
  def click(self):
    if self.on_click:
      self.on_click()

  def on_click(self):
    print('on_click unimplemented')

class Hoverable():
  is_hovered = False

  def mouse_enter(self):
    if not self.is_hovered:
      self.is_hovered = True
      if self.on_mouse_enter:
        self.on_mouse_enter()

  def mouse_exit(self):
    if self.is_hovered:
      self.is_hovered = False
      if self.on_mouse_exit:
        self.on_mouse_exit()

  def on_mouse_enter(self):
    print('on_mouse_enter unimplemented')

  def on_mouse_exit(self):
    print('on_mouse_exit unimplemented')

class Button(Transform, Clickable, Hoverable):
  def __init__(self, x, y, width, height, label, parent=None, font=common.font_18, action=None):
    width = max(width, font.size(label)[0] + 8)
    height = max(height, font.size(label)[1] + 2)

    super().__init__(pygame.Rect(x, y, width, height), parent)

    self.default_colors = ((243, 243, 239), common.color_accent_blue, common.color_text_dark)
    self.highlight_colors = ((216, 230, 242), common.color_accent_blue, common.color_text_dark)
    self.colors = self.default_colors
    self.disabled_colors = ((243, 243, 239), common.color_accent_blue, common.color_bg_dark)

    self.label = label
    self.font = font
    self.action = action

  def draw(self):
    s = self.font.size(self.label)
    
    pygame.draw.rect(common.screen, self.colors[0], self.get_bounds())
    pygame.draw.rect(common.screen, self.colors[1], self.get_bounds(), 1)

    write(self.label, self.get_bounds().x + self.get_bounds().width // 2 - s[0] // 2, self.get_bounds().y + self.get_bounds().height // 2 - s[1] // 2, self.colors[2], self.colors[0], self.font)

    Transform.draw(self)

  def on_click(self):
    if self.action:
      self.action()
    else:
      print(f'Click unimplemented on {self.label}.')

  def on_mouse_enter(self):
    self.colors = self.highlight_colors
    self.draw()

  def on_mouse_exit(self):
    self.colors = self.default_colors
    self.draw()

class Panel(Transform):
  def __init__(self, x, y, width, height, label, parent=None):
    Transform.__init__(self, pygame.Rect(x, y, width, height), parent)
    Hoverable.__init__(self)
    
    self.label = label
    self.font = common.font_18

  def draw(self):
    if self.get_bounds().y > 0:
      pygame.draw.line(common.screen, self.colors[0], (self.get_bounds().x, self.get_bounds().y + 1), (self.get_bounds().x + self.get_bounds().width, self.get_bounds().y + 1), 1)

    pygame.draw.line(common.screen, self.colors[1], (self.get_bounds().x, self.get_bounds().y + self.get_bounds().height), (self.get_bounds().x + self.get_bounds().width, self.get_bounds().y + self.get_bounds().height), 1)

    Transform.draw(self)

class Typeable():
  text = ''

  def add_char(self, char):
    self.text += char

  def del_char(self):
    if len(self.text) > 0:
      self.text = self.text[:-1]
