

from ..utils import ScreenCapture, ScreenMatch, Predict, SaveCapToFile
from .task_center import TaskCenter
from .constants import GameName
from queue import Queue


class Dnf:

    def __init__(self,
                 fps: int,
                 model="netmodels/yolov8/yolov8n.pt",
                 scaling=1.5,
                 dev_model: bool = False,

                 save_capture: bool = False,):

        self.fps = fps
        self.dev_model = dev_model
        self.save_capture = save_capture
        self.model = model
        self.scaling = scaling
        self.save_capture_queue = Queue()
        self._last_screen_snapshot = None
        self.task_queue = Queue()

    @property
    def last_screen_snapshot(self):
        return self._last_screen_snapshot

    @last_screen_snapshot.setter
    def last_screen_snapshot(self, new_img):
        self._last_screen_snapshot = new_img

    def start(self):
        screen_match = ScreenMatch(GameName)

        def capture_callback(img):
            self.last_screen_snapshot = img

        def predict_callback(results):
            self.task_queue.put(results)
            pass

        def predict_source():
            return self.last_screen_snapshot

        if screen_match.size_enable:
            TaskCenter(task_queue=self.task_queue).start()
            Predict(predict_source=predict_source,
                    predict_callback=predict_callback,
                    model=self.model,
                    fps=self.fps,
                    dev_model=self.dev_model
                    ).start()
            if self.save_capture:
                SaveCapToFile(
                    save_capture_queue=self.save_capture_queue,
                    file_name="dnf.png",
                    folder_path="data/images",
                    overtime=20
                ).start()

            screen_capture = ScreenCapture(
                capture_size=screen_match.size,
                capture_callback=capture_callback,
                fps=self.fps,
                dev_model=self.dev_model)

            screen_capture.start()
            screen_capture.join()
            print("main thread end")

        pass


if __name__ == '__main__':

    try:
        # 初始化屏幕截图

        pass
    except Exception as e:
        print(e)
