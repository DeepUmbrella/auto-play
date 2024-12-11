from typing import Callable
import numpy as np
import mss
import time
import cv2
import random
from queue import Queue
from threading import Event, Thread
from .screen_match import ScreenMatch


class ScreenCapture:

    def __init__(self, screen_target: ScreenMatch, fps: int = 5, dev_model: bool = False):
        self._img = None
        self._DEV_MODEL = dev_model
        self.screen_target = screen_target
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

    def producer(self):

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
                self._img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                if self._DEV_MODEL == True:
                    cv2.imshow('Screen Capture', self.img)
                    # 按下 'q' 键退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.capture_stop()
                elapsed_time = time.time() - start_time

                sleep_time = max(0, frame_duration - elapsed_time)
                time.sleep(sleep_time)

    def capture_stop(self):
        self.capturing = False
        pass

    def capture_start(self):
        self.capturing = True
        capture_start_thread = Thread(target=self.producer)
        capture_start_thread.start()
        return capture_start_thread

    def capture_to_file(self):

        import os

        folder_path = "data/images/"
        os.makedirs(folder_path, exist_ok=True)

        while self.capturing:
            # 从队列中获取截图数据
            timestamp = int(time.time() * 1000)
            img_name = f"frame_{timestamp}.png"
            filename = os.path.join(folder_path, img_name)
            cv2.imwrite(filename, self.img)

            print(f"保存文件：{img_name}")
            time.sleep(5)
            pass

    def capture_to_file_start(self, save_capture: bool = False):
        if save_capture:
            capture_to_file_start_thread = Thread(
                target=self.capture_to_file)

            capture_to_file_start_thread.start()
            return capture_to_file_start_thread
