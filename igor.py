# @delay minimum time in seconds between each click
#        chrome browser has trouble handling anything
#        below this number.
#DELAY = 0.2
DELAY = 0.05
DELAY_STEP = 0.01

import win32api, win32con, time, os

# left click at given cordinates
# @_click=1 -> left click
# @_click=2 -> right click
def click (x, y, _click) -> int:
  if _click == 1:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  elif _click == 2:
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
  return 1

# Igor provides what others can't.
# @_click=0 -> left click
# @_click=1 -> right click
def igor (_click):
  a, b = win32api.GetCursorPos()
  ref = a
  timer = time.clock()
  count = 0
  while (ref == a):
    a, b = win32api.GetCursorPos()
    count += click(a, b, _click)
    if (time.clock() - timer > 0.0999999):
      timer = time.clock()
      win32api.SetConsoleTitle("click/s: " + str(count*10))
      count = 0

    time.sleep(DELAY)

def keyboardHandler():
  _click = 0
  _esc = False
  win32api.SetConsoleTitle("paused")
  while (not _esc):
    if (_click > 0):
      igor(_click)
      win32api.SetConsoleTitle("paused")
      print("\033[91m" + "= Cursor movement, stoped clicking." + "\033[0m")

    _click = 0
    _esc = False
    while (not _esc and not _click):
      if (abs(win32api.GetKeyState(120)) > 1):
        _click = 1
        print("\033[92m" + "= F9 pressed, now left clicking!" + "\033[0m")

      elif (abs(win32api.GetKeyState(121)) > 1):
        _click = 2
        print("\033[92m" + "= F10 pressed, now right clicking!" + "\033[0m")

      elif (abs(win32api.GetKeyState(119)) > 1):
        global DELAY
        DELAY += DELAY_STEP
        print("\033[92m" + "= F8 pressed, increasing delay to " + str(DELAY) + "\033[0m")
        time.sleep(0.2)

      elif (abs(win32api.GetKeyState(118)) > 1):
        global delay
        DELAY -= DELAY_STEP
        print("\033[92m" + "= F8 pressed, decreasing delay to " + str(DELAY) + "\033[0m")
        time.sleep(0.2)

      elif (abs(win32api.GetKeyState(0x1B)) > 1):
        _esc = True
        print("= ESC pressed, exiting")

      else:
        time.sleep(0.01)

def main():
  print("========================")
  print("= Welcome " + os.getlogin())
  print("= Move the cursor to pause")
  print("= Clicks/s is displayed in the title.")
  print("=========================")
  print("= Press ESC to exit.")
  print("= Press F7 to decrease time between clicks")
  print("= Press F8 to increase time between clicks")
  print("= Press F9  to begin auto left  clicking")
  print("= Press F10 to begin auto right clicking")
  keyboardHandler()
  print("========================")

if __name__ == "__main__":
  main()
