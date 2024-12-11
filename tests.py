from packages.utils.screen_match import ScreenMatch
from packages.dnf.operation import Operation

from time import sleep


import pyautogui as pg

if __name__ == "__main__":

    target = ScreenMatch("地下城与勇士")
    target.window_active()
    pg.moveTo(947, -1720, duration=2, tween=pg.easeInOutQuad)
    sleep(1)

    operation = Operation()
    operation.trigger_package()
    sleep(3)
    operation.trigger_package()
    # target.window_minimize()
