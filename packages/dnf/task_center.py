from threading import Thread
import queue
import time

# 创建队列

# 创建并启动工作线程


class TaskCenter(Thread):
    def __init__(self, task_queue: queue.Queue):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.task_queue = task_queue

    def run(self):
        while True:
            result = self.task_queue.get()

            result = result.summary()
            print(type(result))
            x = {
                'name': 'jianmo',
                'class': 6,
                'confidence': 0.81737,
                'box': {
                    'x1': 504.17981,
                    'y1': 315.19302,
                    'x2': 622.6344,
                    'y2': 447.62616
                }}
            print(f'Worker {self.name} is processing task {result}')

            # * normalized_data

            # *

            # tensors = task[0].boxes.xywh[0]
            # x, y, w, h = tensors[0].item(), tensors[1].item(
            # ), tensors[2].item(), tensors[3].item()
            # print(
            #     f'Worker {self.name} is processing x : {x}, y : {y}, w : {w}, h : {h}')

            # print(f'Worker {self.name} has finished task {task}')
