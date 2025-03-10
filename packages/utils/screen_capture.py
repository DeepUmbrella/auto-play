
from queue import Queue
import numpy as np
import mss
import time
import cv2
from threading import Thread
from typing import Callable


class ScreenCapture(Thread):

    def __init__(self, capture_size: tuple,
                 predict_source_queue: Queue,
                 pressed_key: Callable[..., any] = lambda *args: None,
                 fps: int = 5,
                 dev_model: bool = False,
                 name="capture"
                 ):

        super().__init__()  # 确保调用父类的初始化方法
        self.name = name
        self._img = None
        self._DEV_MODEL = dev_model
        self.capture_size = capture_size
        self.predict_source_queue = predict_source_queue
        self.pressed_key = pressed_key
        self.fps = fps
        self._act_fps = 0
        self.capturing = False
        self.print_log = False

    @property
    def act_fps(self):
        return self._act_fps

    @property
    def img(self):
        return self._img

    def run(self):
        last_key = None
        with mss.mss() as sct:

            frame_duration = 1 / self.fps
            size = self.capture_size
            monitor = {"top": size[1], "left": size[0],
                       "width": size[2], "height": size[3]}
            print(size, "start capture size")
            while True:
                start_time = time.time()
                screenshot = sct.grab(monitor)

                img = np.array(screenshot)
                # to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                self.predict_source_queue.put(img)

                if self._DEV_MODEL == True:
                    cv2.imshow('Screen Capture', img)
                    # 按下 'q' 键退出
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    if key != 255 and key != last_key:
                        self.pressed_key(key)
                elapsed_time = time.time() - start_time

                sleep_time = max(0, frame_duration - elapsed_time)
                time.sleep(sleep_time)

        print("capture end")

    def capture_stop(self):
        self.capturing = False
        pass


if __name__ == '__main__':
    capture = ScreenCapture((0, 0, 1920, 1080), fps=5, dev_model=True)
    capture.start()
