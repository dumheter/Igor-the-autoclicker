# TODO
# * Don't use sleep
# * Count cps

import win32api, win32con, time

# left click at given cordinates
def click (x, y):
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

# Igor provides what others can't.
def igor ():
    a, b = win32api.GetCursorPos()
    ref = a
    while (ref == a):
        a, b = win32api.GetCursorPos()
        click(a, b)
        time.sleep(0.001) #minumum os sleeptime is enugh

def main ():
    print("==========================")
    print("=== Move the mouse to exit")
    igor()
    print("==========================")
    exit(1)

if __name__ == "__main__":
    main()
