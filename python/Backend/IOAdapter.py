import ctypes
import time
import pyautogui as pg
import mss
import numpy as np

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
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


adapter_dict_1 = {
    'a': 0x1C,
    'b': 0x32, #buff
    'd': 0x23,
    'e': 0x24,
    'h': 0x33, #heal
    'j': 0x3B, #mana
    'r': 0x2D, #mount
    's': 0x1B,
    't': 0x2C, #throw
    'w': 0x1D,
    '1': 0x16,
    '2': 0x1E,
    '3': 0x26,
    '4': 0x25,
    '5': 0x2E,
    '6': 0x36,
    '7': 0x3D,
    '8': 0x3E,
    '9': 0x46,
    '0': 0x45,
    'esc': 0x76,
    'enter': 0x5A,
    'lctrl': 0x14,
    'lshift': 0x12,
    'space': 0x29,
    'default': 0x00,
}

adapter_dict_2 = {
    'a': 0x1E,
    'b': 0x30,  # buff
    'd': 0x20,
    'e': 0x12,
    'h': 0x23,  # heal
    'j': 0x24,  # mana
    'r': 0x13,  # mount
    's': 0x1F,
    't': 0x14,  # throw
    'w': 0x11,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'esc': 0x01,
    'enter': 0x1C,
    'lctrl': 0x1D, #maybe applicable to only non-us keyboards
    'lshift': 0x2A, #maybe applicable to only non-us keyboards
    'space': 0x39,
    'default': 0x00,
}


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


class IOAdapter:
    def __init__(self):
        self.adapter_dict = adapter_dict_2

        self.capture_device = mss.mss()
        self.monitor_dim = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080} #TODO: do this dynamically per monitor
        self.center_x = self.monitor_dim['left'] + int(self.monitor_dim['width'] / 2)
        self.center_y = self.monitor_dim['top'] + int(self.monitor_dim['height'] / 2)

    def get_available_keys(self):
        return list(self.adapter_dict.keys())

    def key(self, key, duration=.1):
        # for efficiency, doesn't call into other class functions since they also do checks for key existence
        if key in self.adapter_dict:
            PressKey(self.adapter_dict[key])
            time.sleep(duration)
            ReleaseKey(self.adapter_dict[key])

    def key_down(self, key):
        if key in self.adapter_dict:
            print('pressing key ' + key)
            PressKey(self.adapter_dict[key])

    def key_up(self, key):
        if key in self.adapter_dict:
            print('releasing key ' + key)
            ReleaseKey(self.adapter_dict[key])

    def mouse_move_relative(self, x, y, duration=None):
        print('moving mouse')
        if duration is None:
            pg.moveTo(x + self.center_x, y + self.center_y)
        else:
            pg.moveTo(x + self.center_x, y + self.center_y, duration)

    def left_mouse_down(self):
        pg.mouseDown()

    def left_mouse_up(self):
        pg.mouseUp()

    def left_click(self):
        pg.click()

    def right_mouse_down(self):
        pg.mouseDown()

    def right_mouse_up(self):
        pg.mouseUp()

    def right_click(self):
        pg.click()

    def get_screen(self):
        return np.array(self.capture_device.grab(self.monitor_dim))