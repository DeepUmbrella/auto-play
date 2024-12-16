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

    def run(self):
        while True:
            task = task_queue.get()
            print(f'Worker {self.name} is processing task {task}')
            time.sleep(10)
            print(f'Worker {self.name} has finished task {task}')
