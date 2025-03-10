

from ..utils import ScreenCapture, ScreenMatch, Predict, SaveCapToFile
from .task_center import TaskCenter
from .constants import GameName
from queue import Queue


class Dnf:

    def __init__(self,
                 fps: int,
                 model="netmodels/yolov8/yolov8n.pt",
                 scaling=1.5,
                 dev_model: bool = False):

        self.fps = fps
        self.dev_model = dev_model
        self.model = model
        self.scaling = scaling
        self.predict_source_queue = Queue(maxsize=10)
        self.predict_results_queue = Queue(maxsize=10)

    def start(self):
        screen_match = ScreenMatch(GameName)

        if screen_match.size_enable:
            TaskCenter(
                result_queue=self.predict_results_queue,
            ).start()

            Predict(
                predict_source_queue=self.predict_source_queue,
                predict_results_queue=self.predict_results_queue,
                model=self.model,
                fps=self.fps,
            ).start()

            screen_capture = ScreenCapture(
                capture_size=screen_match.size,
                predict_source_queue=self.predict_source_queue,
                fps=self.fps,
                dev_model=self.dev_model
            )

            screen_capture.start()
            screen_capture.join()

        pass


if __name__ == '__main__':

    try:
        # 初始化屏幕截图

        pass
    except Exception as e:
        print(e)
