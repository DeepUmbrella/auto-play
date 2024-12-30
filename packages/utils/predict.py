from torch import torch
from ultralytics import YOLO
from threading import Thread
import time
from typing import Callable


class Predict(Thread):
    def __init__(self,
                 predict_source: Callable[[], None] = lambda: any,
                 predict_callback: Callable[..., None] = lambda: None,
                 daemon=True,
                 fps=30,
                 model="netmodels/yolov8/yolov8n.pt"):

        super().__init__()
        self.daemon = daemon
        self.model = YOLO(model, verbose=False)
        self.predict_source = predict_source
        self.predict_callback = predict_callback
        self.fps = fps
        self.selectDevice()

    def selectDevice(self):
        if torch.cuda.is_available():
            self.model.to("cuda")

    def run(self):

        frame_duration = 1 / self.fps

        while True:
            start_time = time.time()
            img_source = self.predict_source()

            if img_source is not None:
                result = self.model.predict(img_source, verbose=False)[0]
                self.predict_callback(result)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_duration - elapsed_time)
            time.sleep(sleep_time)
