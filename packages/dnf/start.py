

from ..utils import ScreenCapture
from ..utils import ScreenMatch
from ..utils import Predict
from .operation_queue import task_queue, Worker
from .constants import GameName


class Dnf:

    def __init__(self,
                 fps: int,
                 model="netmodels/yolov8/yolov8n.pt",
                 scaling=1.5,
                 cap_dev_model: bool = False,
                 predict_dev_model: bool = False,
                 save_capture: bool = False,):

        self.fps = fps
        self.cap_dev_model = cap_dev_model
        self.predict_dev_model = predict_dev_model
        self.save_capture = save_capture
        self.screen_match = ScreenMatch(GameName)
        self.model = model
        self.scaling = scaling

        pass

    def start(self):

        if self.screen_match.size_enable:
            worker = Worker()
            screen_capture = ScreenCapture(
                self.screen_match, fps=self.fps, dev_model=self.cap_dev_model)
            predict = Predict(screen_capture,
                              predict_callback=task_queue.put,
                              model=self.model,
                              dev_model=self.predict_dev_model)

            worker_th = worker.start()
            capture_th = screen_capture.capture_start()
            save_img_th = screen_capture.capture_to_file_start(
                save_capture=self.save_capture)
            predict_th = predict.predict_start()
            worker_th.join()
            capture_th.join()
            if save_img_th is not None:
                save_img_th.join()
            predict_th.join()
        pass


if __name__ == '__main__':

    try:
        # 初始化屏幕截图

        pass
    except Exception as e:
        print(e)
