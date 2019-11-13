import pyautogui as pg
import time


import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# # directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# while (True):
#     PressKey(0x11)
#     time.sleep(1)
#     ReleaseKey(0x11)
#     time.sleep(1)


def run():
    key_1 = 0x02
    key_2 = 0x03

    key_a = 0x1E


    middle_x = int(1920 / 2)
    middle_y = int(1080 / 2)

    time.sleep(5)

    print('staring keys 1')

    PressKey(key_1)
    time.sleep(.1)
    ReleaseKey(key_1)
    time.sleep(1)

    PressKey(key_2)
    time.sleep(.1)
    ReleaseKey(key_2)
    time.sleep(1)

    PressKey(key_a)
    time.sleep(3)
    ReleaseKey(key_a)
    time.sleep(1)

    print('starting keys')

    pg.press('1')
    time.sleep(1)
    pg.press('2')
    time.sleep(1)
    pg.press('3')
    time.sleep(3)

    pg.keyDown('w')
    time.sleep(3)
    pg.keyUp('w')
    time.sleep(1)

    print('starting mouse')

    pg.moveTo(middle_x, middle_y, 1)
    time.sleep(1)
    pg.moveTo(middle_x, middle_y + 50, 1)
    pg.mouseDown()
    time.sleep(5)
    pg.mouseUp()

if __name__=='__main__':
    run()