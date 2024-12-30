from threading import Thread
import queue
import cv2
from .skill_area import Skill

# 创建队列

# 创建并启动工作线程
skill = Skill(320, 100, 0, 5, 1, 0)


class TaskCenter(Thread):
    def __init__(self, task_queue: queue.Queue, dev_model: bool = False):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.task_queue = task_queue
        self.dev_model = dev_model

    def run(self):
        while True:
            result = self.task_queue.get()
            img = result.plot().copy()
            boxes = result.boxes
            detected = len(boxes) != 0

            if detected:

                box = result.boxes[0]

                data = box.data

                data0 = data[0]

                data00 = data0.cpu().numpy()

                x1, y1, x2, y2, cof, cls = data00

                center_coordinates = (
                    int((x1 + x2) / 2), int((y1 + y2) / 2))

                x1, y1, x2, y2 = skill.calculate_area_coordinates(
                    center_coordinates[0], center_coordinates[1])
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

                print(x1, y1, x2, y2, cof, cls, 66666)
            if self.dev_model == True:
                if detected:
                    cv2.rectangle(img, (x1, y1),
                                  (x2, y2), (0, 255, 0), 2)
                cv2.imshow('predict', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
