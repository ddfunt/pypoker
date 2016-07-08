import win32api
import win32gui
import win32process
from PIL import ImageGrab
import os
import time
import ctypes
import subprocess
import pyautogui
from poker.server.client import send
import pickle


from poker.paths import Paths



card_pos = [
            (400,279),
            (477,279),
            (554,279),
            (626,279),
            (701,279),
            ]

class GameWindow:

    def __init__(self,title='No Limit'):
        self.hwid = self.get_window(title)
        self.x, self.y, self.width, self.height = win32gui.GetWindowRect(self.hwid)
        self.set_active()

    def set_active(self):
        win32gui.SetForegroundWindow(self.hwid)
        _, pid = win32process.GetWindowThreadProcessId(self.hwid)
        print(_, pid)
        #win32gui.SetFocus(self.hwid)
        win32gui.MoveWindow(self.hwid, 0, 0, 1100, 900, False)

    @staticmethod
    def get_window(search_key):
        def windowEnumerationHandler(hwnd, top_windows):
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        results = []
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for window in top_windows:
            #if win32gui.IsWindowVisible(window[0]):
            #    print(window)
            if search_key in window[1]:
                results.append(window)
        if len(results) == 1:
            print(results)
            return results[0][0]
        else:
            raise ValueError('NO WINDOW FOUND')


def screenGrab():
    im_path  = Paths.image_path()
    box = ()
    im = ImageGrab.grab()
    im.save(im_path, 'PNG')
    return im

def check_turn(image):
    card = 255
    color = [True if all(x == card for x in image.getpixel(pos))  else False for pos in card_pos ]
    if color[-1]:
        return 'river'
    elif color[-2]:
        return 'turn'
    elif color[-3]:
        return 'flop'
    else:
        return 'preflop'

def mousePos(x,y):
    win32api.SetCursorPos((x,y))


def write_mouse_move(x, y, hwid):
    print(os.path.exists(Paths.ahk_path()))
    with open(os.path.join(Paths.ahk_path(), 'test.ahk'), 'w') as f:
        #f.write('#InstallKeybdHook\n#UseHook On\n')
        #f.write('MouseMove, %i, %i\n' % (int(x), int(y)))
        #f.write('CLick')
        f.write('PostMessage, 0x200, 0, %s&0xFFFF | %s<<16, , %s ; WM_MOUSEMOVE\n' %(x,y,hwid))
        f.write('PostMessage, 0x201, 0, %s&0xFFFF | %s<<16, , %s ; WM_LBUTTONDOWN\n' %(x,y,hwid))
        f.write('PostMessage, 0x202, 0, %s&0xFFFF | %s<<16, , %s ; WM_LBUTTONUP\n' %(x,y,hwid))

def run_ahk():
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #subprocess.call([spcatpath, filepath])#, shell=True)
    subprocess.call('"%s" "%s"' % (os.path.join(Paths.ahk_path(), 'AutoHotkey.exe'),
                                   os.path.join(Paths.ahk_path(), 'test.ahk')), shell=True)


def get_pot(image):
    im = image.crop((475, 236, 649, 264))
    im.save('test.png')

    return im
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
#while (True):
import time

if __name__ == '__main__':
    import time
    #time.sleep(3)
    x = GameWindow('No Limit')
    im = screenGrab()
    print(check_turn(im))
    print(im.size)
    pot_image = get_pot(im)

    print(send(pickle.dumps(pot_image)))


    #while True:
    #    print(win32api.GetCursorPos())

"""
475 236
640, 236
475, 264
640, 264
"""

"""
ControlClick2(X, Y, WinTitle="", WinText="", ExcludeTitle="", ExcludeText="")
{
  hwnd:=ControlFromPoint(X, Y, WinTitle, WinText, cX, cY
                             , ExcludeTitle, ExcludeText)
  PostMessage, 0x200, 0, cX&0xFFFF | cY<<16,w, ahk_id %hwnd% ; WM_MOUSEMOVE
  PostMessage, 0x201, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_LBUTTONDOWN
  PostMessage, 0x202, 0, cX&0xFFFF | cY<<16,, ahk_id %hwnd% ; WM_LBUTTONUP
}
"""