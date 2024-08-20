
import numpy as np
import mss
import time
import cv2


class ScreenCapture:

    def __init__(self, left=None, top=None, width=None, height=None):
        self.monitor = 1
        self.fps = 30
        self.act_fps = 0

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

    def capture_window(self, dev=False):

        with mss.mss() as sct:

            frame_duration = 1 / self.fps

            while True:
                start_time = time.time()
                # 从显示器捕获图像
                screenshot = sct.grab(self.size)

                # 将图像转换为NumPy数组
                img = np.array(screenshot)

                # 转换为BGR格式（OpenCV默认颜色格式）
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                if dev == True:
                    cv2.imshow('Screen Capture', img)

                    # 按下 'q' 键退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    # 计算需要睡眠的时间以保持 60 FPS

                    pass

                elapsed_time = time.time() - start_time
                self.act_fps = 1 / elapsed_time
                sleep_time = max(0, frame_duration - elapsed_time)
                time.sleep(sleep_time)

            cv2.destroyAllWindows()

    def start_capture(self, output_url: str, fps=30):

        pass

    def start_capture(self, fps=30):
        pass
