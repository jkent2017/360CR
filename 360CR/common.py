import pygame

black = (12,12,12)
dark_gray = (18,18,18)
gray = (72,72,72)
white = (240,240,240)
blue = (94,115,219)
red = (240,32,60)
yellow = (250,208,32)

width = 800
height = 600

spacing_lg = 6
spacing_sm = 4
border = 2

font_18 = None
font_16 = None
font_14 = None
font_12 = None
font_mono = None
screen = None

panel_message_width = width
panel_message_height = 100
panel_message_x = 0
panel_message_y = height - panel_message_height
panel_message_label = 'Application Log'

panel_camera_width = height - panel_message_height - 30
panel_camera_height = height - panel_message_height - 30
panel_camera_x = width - panel_camera_width
panel_camera_y = 15
panel_camera_label = 'Camera'

panel_control_width = width - panel_camera_width
panel_control_height = height - panel_message_height - 30
panel_control_x = 0
panel_control_y = 15
panel_control_label = 'Settings'

panel_mapping_width = 200
panel_mapping_height = 150
panel_mapping_label = 'Mapping'

# PS DUALSHOCK 4 MAPPING
BUTTON_A  =  0
BUTTON_B  =  1
BUTTON_Y  =  2
BUTTON_X  =  3
BUTTON_LB =  4
BUTTON_RB =  5
BUTTON_LT =  6
BUTTON_RT =  7
BUTTON_SL =  8
BUTTON_ST =  9
BUTTON_PS = 10
BUTTON_LS = 11
BUTTON_RS = 12

AXIS_LS_H = 0
AXIS_LS_V = 1
AXIS_LT   = 2
AXIS_RS_H = 3
AXIS_RS_V = 4
AXIS_RT   = 5