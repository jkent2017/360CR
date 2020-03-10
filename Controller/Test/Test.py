import os
import re

rootdir = "/dev/"
regex = re.compile('cu.usbmodem*')

for root, dirs, files in os.walk(rootdir):
  for file in files:
    if regex.match(file):
      serial = rootdir + file
      print("\\" + serial + "\\")