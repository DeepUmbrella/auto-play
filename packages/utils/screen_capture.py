from typing import Callable
import numpy as np
import mss
import time
import cv2
from queue import Queue
from threading import Event
from .screen_match import ScreenMatch


class ScreenCapture:

    def __init__(self, screen_target: ScreenMatch, fps: int = 3, dev_model: bool = False):
        self._DEV_MODEL = dev_model
        self.screen_target = screen_target
        self.fps = fps
        self._act_fps = 0
        self.capturing = False
        self.print_log = False

    @property
    def act_fps(self):
        return self._act_fps

    def producer(self):
        self.capturing = True

        with mss.mss() as sct:

            frame_duration = 1 / self.fps
            size = self.screen_target.size
            monitor = {"top": size[1], "left": size[0],
                       "width": size[2], "height": size[3]}
            print(size, "start capture size")
            while self.capturing:
                start_time = time.time()
                screenshot = sct.grab(monitor)

                img = np.array(screenshot)

                # to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                if self._DEV_MODEL == True:
                    cv2.imshow('Screen Capture', img)
                    # 按下 'q' 键退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.capture_stop()
                elapsed_time = time.time() - start_time
                self._act_fps = 1 / elapsed_time
                sleep_time = max(0, frame_duration - elapsed_time)
                time.sleep(sleep_time)

    def capture_stop(self):
        self.capturing = False
        pass

    def capture_start(self):
        self.capturing = True
        self.producer()
        pass
