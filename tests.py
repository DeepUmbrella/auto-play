from packages.utils.screen_match import ScreenMatch
from packages.dnf.operation import Operation
from packages.utils.keydirect import key_down, key_up, PressKey, ReleaseKey

from time import sleep


import pyautogui as pg

if __name__ == "__main__":
    from pynput.mouse import Controller, Button as MouseButton
    from pynput.keyboard import Controller as KeyboardController

    # 鼠标移动到特定位置

    target = ScreenMatch("地下城与勇士")

    if not target.window_is_active:
        target.window_active()
        pass
        # count = 1
    sleep(2)

    # while True:

    #     keyboard.press('a'),
    #     sleep(0.02)
    #     keyboard.release('a')

    #     print(f"按了a:第{count}次")

    #     sleep(4)
    key_down("k")
    sleep(0.02)
    key_up("k")
    #     print(f"按了K:第{count}次")

    #     count += 1
    #     sleep(4)

    # mouse.move(-500, -500)

    # # mouse.position = (947, -1720)
    # mouse.click(MouseButton.right, 1)
    # # 按下键盘上的 'a' 键

    # target.window_minimize()
