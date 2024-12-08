from torch import torch
from ultralytics import YOLO
from queue import Queue
import cv2
from threading import Event


# Load a model
# model = YOLO("netmodels/yolov8/yolov8n.pt")
# model = YOLO("netmodels/yolov8/yolov8n.pt")


class Predict:
    def __init__(self, sourceQueue: Queue, model="netmodels/yolov8/yolov8n-pose.pt"):
        self.model = YOLO(model)
        self.sourceQueue = sourceQueue
        self.selectDevice()

    def selectDevice(self):
        if torch.cuda.is_available():
            self.model.to("cuda")

    def set_show_img_window_size(self, width, height):
        if width is not None and height is not None:
            cv2.namedWindow('predict', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('predict', width, height)

    def consumer(self, img, dev=True):
        while True:
            results = self.model(img)
            if dev == True:
                for result in results:
                    boxes = result.boxes  # Boxes object for bounding box outputs
                    masks = result.masks  # Masks object for segmentation masks outputs
                    keypoints = result.keypoints  # Keypoints object for pose outputs
                    probs = result.probs  # Probs object for classification outputs
                    obb = result.obb  # Oriented boxes object for OBB outputs
                cv2.imgshow('predict', results[0].plot())
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyWindow('predict')
