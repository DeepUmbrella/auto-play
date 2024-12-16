from torch import torch
from ultralytics import YOLO
import cv2
from threading import Thread
import time
from typing import Callable

# Load a model
# model = YOLO("netmodels/yolov8/yolov8n.pt")
# model = YOLO("netmodels/yolov8/yolov8n.pt")


class Predict(Thread):
    def __init__(self,
                 predict_source: Callable[[], None] = lambda: any,
                 predict_callback: Callable[..., None] = lambda: None,
                 dev_model=False,
                 daemon=True,
                 fps=30,
                 model="netmodels/yolov8/yolov8n.pt"):

        super().__init__()
        self.daemon = daemon
        self.model = YOLO(model)
        self.dev_model = dev_model
        self.predict_source = predict_source
        self.predict_callback = predict_callback
        self.fps = fps
        self.selectDevice()

    def selectDevice(self):
        if torch.cuda.is_available():
            self.model.to("cuda")

    def set_show_img_window_size(self, width, height):
        if width is not None and height is not None:
            cv2.namedWindow('predict', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('predict', width, height)

    def run(self):
        frame_duration = 1 / self.fps

        while True:
            start_time = time.time()
            img_source = self.predict_source()
            if img_source is not None:

                results = self.model(img_source)

                if self.dev_model == True:

                    for result in results:
                        boxes = result.boxes  # Boxes object for bounding box outputs
                        masks = result.masks  # Masks object for segmentation masks outputs
                        keypoints = result.keypoints  # Keypoints object for pose outputs
                        probs = result.probs  # Probs object for classification outputs
                        obb = result.obb  # Oriented boxes object for OBB outputs
                    self.predict_callback(results)
                    cv2.imshow('predict', results[0].plot())
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_duration - elapsed_time)
            time.sleep(sleep_time)

        cv2.destroyWindow('predict')
