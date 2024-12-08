

from ..utils import ScreenCapture
from ..utils import ScreenMatch
from ..utils.predict import Predict

from .constants import GameName
import queue
import threading


class Dnf:

    def __init__(self):
        pass

    def start(self):
        screen_match = ScreenMatch(GameName)
        if screen_match.size_enable:

            screen_capture = ScreenCapture(screen_match, dev_model=True)
            screen_capture.capture_start()

        pass


if __name__ == '__main__':

    try:
        # 初始化屏幕截图

        pass
    except Exception as e:
        print(e)
