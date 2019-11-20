import os
import sys

import win32api
import win32process
import win32gui
import win32con
import time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))



from Action import ActionManager
from IOAdapter import IOAdapter


def print_handle(val):
    print(f'+ {val} ')

def test():
    io = IOAdapter()
    # processes = win32process.EnumProcesses()
    handle1 = win32gui.FindWindow(None, "TerrarAI: 8001")
    handle2 = win32gui.FindWindow(None, "TerrarAI: 8002")
    print(handle1)
    print(handle2)
    # handle = win32gui.FindWindow(None, "*Untitled - Notepad")
    win32gui.SetForegroundWindow(handle1)
    io.key_down('a')
    time.sleep(1)
    win32gui.SetForegroundWindow(handle2)
    io.key_down('d')
    time.sleep(1)
    io.key_up('d')
    win32gui.SetForegroundWindow(handle1)
    io.key_up('a')
    # key_to_send = 0x41
    # time.sleep(1)
    # for i in range(0xFF):
    #     res = win32api.PostMessage(handle, win32con.WM_KEYDOWN, key_to_send, 0)
    #     # print(f'{res} - {i}')
    #     # print(win32api.GetLastError())
    #     time.sleep(.05)
    #     win32api.PostMessage(handle, win32con.WM_KEYUP, key_to_send, 0)


    # while(True):
    #
    #     # print(win32api.PostMessage(handle, win32con.WM_CHAR, key_to_send, 0))
    #     print(win32api.SendMessage(handle, win32con.WM_CHAR, key_to_send, 0))
    #     time.sleep(1)
    #     # print(win32api.PostMessage(handle, win32con.WM_KEYUP, key_to_send, 0))
    #     time.sleep(1)




if __name__=='__main__':
    test()
