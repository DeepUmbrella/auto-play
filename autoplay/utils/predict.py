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

    def consumer(self, queue: Queue, stop_signal: Event, dev=True):
        while not stop_signal.is_set():
            img = queue.get()
            results = self.model(img)
            if dev == True:
                for result in results:
                    boxes = result.boxes  # Boxes object for bounding box outputs
                    masks = result.masks  # Masks object for segmentation masks outputs
                    keypoints = result.keypoints  # Keypoints object for pose outputs
                    probs = result.probs  # Probs object for classification outputs
                    obb = result.obb  # Oriented boxes object for OBB outputs
                cv2.imshow('predict', results[0].plot())
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyWindow('predict')
