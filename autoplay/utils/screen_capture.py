from typing import Callable
import numpy as np
import mss
import time
import cv2
from queue import Queue
from threading import Event


class ScreenCapture:

    def __init__(self, left=None, top=None, width=None, height=None):
        self.monitor = 1
        self.fps = 60
        self._act_fps = 0
        self.capturing = False
        self.print_log = False

        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor]
            screen_width = monitor["width"]
            screen_height = monitor["height"]

        self.size = {
            "left": left if left is not None else 0,
            "top": top if top is not None else 0,
            "width": width if width is not None else screen_width,
            "height": height if height is not None else screen_height,
        }

    def get_size(self):
        return self.size

    def set_size(self, left=None, top=None, width=None, height=None):
        if left is not None:
            self.size["left"] = left
        if top is not None:
            self.size["top"] = top
        if width is not None:
            self.size["width"] = width
        if height is not None:
            self.size["height"] = height

    def producer(self, queue: Queue, stop_signal: Event, dev=False):
        self.capturing = True
        with mss.mss() as sct:

            frame_duration = 1 / self.fps

            while self.capturing:
                start_time = time.time()
                screenshot = sct.grab(self.size)

                img = np.array(screenshot)
                # to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                queue.put(img)

                # results = model(img, verbose=self.print_log)
                # frame = results[0].plot()

                # # boxes = result.boxes  # Boxes object for bounding box outputs
                # # masks = result.masks  # Masks object for segmentation masks outputs
                # # keypoints = result.keypoints  # Keypoints object for pose outputs
                # # probs = result.probs  # Probs object for classification outputs
                # # obb = result.obb

                if dev == True:
                    cv2.imshow('Screen Capture', img)
                    # 按下 'q' 键退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.capture_stop()
                elapsed_time = time.time() - start_time
                self._act_fps = 1 / elapsed_time
                sleep_time = max(0, frame_duration - elapsed_time)
                time.sleep(sleep_time)

        stop_signal.set()

    def capture_stop(self):
        self.capturing = False
        pass

    @property
    def act_fps(self):
        return self._act_fps
