# MIT License
#
# Copyright (c) 2019 Christoffer Gustafsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

##########################################################
# Imports
##########################################################

import win32api, win32con, time, os


##########################################################
# Globals
##########################################################

kDelay = 0.05
kDelayStep = 0.005

VK_ESCAPE = 0x1b
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7a
VK_F12 = 0x7b


##########################################################
# Functions
##########################################################

def click (x, y, _click) -> int:
  """
  left click at given cordinates
  @param _click 1 -> left click
                2 -> right click
  """
  if _click == 1:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  elif _click == 2:
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
  return 1


def IsKeyDown(virtual_key):
  """
  Check if the key is down
  """
  return abs(win32api.GetKeyState(virtual_key)) > 1


def igor (_click, stop_on_mouse_move):
  """
  Igor provides what others can't.
  @param _click 0 -> left click
                1 -> right click
  @param stop_on_mouse_move [bool]
  """
  a, b = win32api.GetCursorPos()
  ref = a
  timer = time.clock()
  count = 0
  run = True
  while (run):
    if (stop_on_mouse_move and ref != a):
      run = False
    elif (IsKeyDown(VK_F4)):
      run = False
      time.sleep(1) # to not instantly change the stop action

    a, b = win32api.GetCursorPos()
    count += click(a, b, _click)
    if (time.clock() - timer > 0.0999999):
      timer = time.clock()
      win32api.SetConsoleTitle("click/s: " + str(count*10))
      count = 0

    time.sleep(kDelay)


def keyboardHandler():
  """
  Igor specific keyboard handling.
  """
  _click = 0
  _esc = False
  mouse_as_stop_action = True
  win32api.SetConsoleTitle("paused")
  while (not _esc):
    if (_click > 0):
      igor(_click, mouse_as_stop_action)
      win32api.SetConsoleTitle("paused")
      print("\033[91m" + "= Cursor movement, stoped clicking." + "\033[0m")

    _click = 0
    _esc = False
    while (not _esc and not _click):
      if (IsKeyDown(VK_F9)):
        _click = 1
        print("\033[92m" + "= F9 pressed, now left clicking!" + "\033[0m")

      elif (IsKeyDown(VK_F10)):
        _click = 2
        print("\033[92m" + "= F10 pressed, now right clicking!" + "\033[0m")

      elif (IsKeyDown(VK_F8)):
        global kDelay
        kDelay += kDelayStep
        print("\033[92m" + "= F8 pressed, increasing delay to " + str(kDelay) + "\033[0m")
        time.sleep(0.2)

      elif (IsKeyDown(VK_F7)):
        global delay
        kDelay -= kDelayStep
        print("\033[92m" + "= F7 pressed, decreasing delay to " + str(kDelay) + "\033[0m")
        time.sleep(0.2)

      elif (IsKeyDown(VK_F4)):
        mouse_as_stop_action = not mouse_as_stop_action
        state = ""
        if (mouse_as_stop_action):
          state = "[mouse move]"
        else:
          state = "[press F4]"
        print("\033[92m" + "= F4 pressed, stop action is now " + state + "\033[0m")
        time.sleep(0.2)

      elif (IsKeyDown(VK_ESCAPE)):
        _esc = True
        print("= ESC pressed, exiting")

      else:
        time.sleep(0.01)


##########################################################
# Main
##########################################################

def main():
  print("========================")
  print("= Welcome " + os.getlogin())
  print("= Move the cursor to pause (stop action is [mouse move])")
  print("= Clicks/s is displayed in the title.")
  print("=========================")
  print("= Press ESC to exit.")
  print("= Press F4 to toggle [mouse move] or [press F4] as stop action")
  print("= Press F7 to decrease time between clicks")
  print("= Press F8 to increase time between clicks")
  print("= Press F9  to begin auto left  clicking")
  print("= Press F10 to begin auto right clicking")
  keyboardHandler()
  print("========================")

if __name__ == "__main__":
  main()
