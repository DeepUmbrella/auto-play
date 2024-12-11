from torch import torch
from ultralytics import YOLO
from queue import Queue
import cv2
from threading import Event, Thread
from .screen_capture import ScreenCapture
import time
from typing import Callable

# Load a model
# model = YOLO("netmodels/yolov8/yolov8n.pt")
# model = YOLO("netmodels/yolov8/yolov8n.pt")


class Predict:
    def __init__(self,
                 screen_capture: ScreenCapture,
                 predict_callback: Callable[..., None] = lambda: None,
                 dev_model=False,
                 model="netmodels/yolov8/yolov8n.pt"):
        self.model = YOLO(model)
        self.dev_model = dev_model
        self.screen_capture = screen_capture
        self.predict_callback = predict_callback
        self.selectDevice()

    def selectDevice(self):
        if torch.cuda.is_available():
            self.model.to("cuda")

    def set_show_img_window_size(self, width, height):
        if width is not None and height is not None:
            cv2.namedWindow('predict', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('predict', width, height)

    def consumer(self):
        frame_duration = 1 / self.screen_capture.fps

        while self.screen_capture.capturing:
            start_time = time.time()
            if self.screen_capture.img is not None:

                results = self.model(self.screen_capture.img)

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
                        self.screen_capture.capturing = False
            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_duration - elapsed_time)
            time.sleep(sleep_time)

        cv2.destroyWindow('predict')

    def predict_start(self):
        predict_start_thread = Thread(target=self.consumer)
        predict_start_thread.start()
        return predict_start_thread
