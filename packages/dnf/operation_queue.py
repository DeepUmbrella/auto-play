import threading
import queue
import time

# 创建队列
task_queue = queue.Queue()

# 创建并启动工作线程


class Worker(threading.Thread):
    def run(self):
        while True:
            task = task_queue.get()
            print(f'Worker {self.name} is processing task {task}')
            time.sleep(1)
            print(f'Worker {self.name} has finished task {task}')
