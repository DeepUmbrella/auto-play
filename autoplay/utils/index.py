from torch import torch
from ultralytics import YOLO


# Load a model
model = YOLO("netmodels/yolov8/yolov8n.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
# return a list of Results objects
results = model(["data/traning/test/input/im1.webp",
                "data/traning/test/input/im2.jpg"])

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk
