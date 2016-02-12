# @delay minimum time in seconds between each click
#        chrome browser has trouble handling anything
#        below this number.
DELAY = 0.001

import win32api, win32con, win32console, time

# left click at given cordinates
def click (x, y):
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  return 1

# Igor provides what others can't.
def igor ():
  a, b = win32api.GetCursorPos()
  ref = a
  timer = time.clock()
  count = 0
  while (ref == a):
    a, b = win32api.GetCursorPos()
    count += click(a, b)
    if (time.clock() - timer > 0.0999999):
      timer = time.clock()
      win32console.SetConsoleTitle("click/s: " + str(count*10))
      count = 0
        
    time.sleep(DELAY)

def keyboardHandler():
  _click = _esc = False
  while (not _esc):
    _click = _esc = False
    igor()
    while (not _esc and not _click):
      if (abs(win32api.GetKeyState(120)) > 1):
        _click = True
        print("= F9 pressed, resuming")

      if (abs(win32api.GetKeyState(0x1B)) > 1):
        _esc = True
        print("= ESC pressed, exiting")      
    
def main ():
  print("========================")
  print("= Welcome " + win32api.GetComputerName())
  print("= Move the mouse to exit")
  print("= Clicks/s in title")
  print("========================")
  print("= To resume, press F9")
  print("= To exit, press esc")
  keyboardHandler()
  print("========================")
  exit(1)

if __name__ == "__main__":
  main()
