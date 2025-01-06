from threading import Thread
import queue
from typing import List, Callable


class TaskCenter(Thread):
    def __init__(self, result_queue: queue.Queue, runList: List[Callable] = None):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.result_queue = result_queue
        self.runList = runList

    def executeRunList(self, initial_input):
        for func in self.runList:
            if callable(func):
                initial_input = func(initial_input)
        pass

    def run(self):
        if len(self.runList) == 0 or self.runList is None:
            print("No task to run, exit")
            return

        while True:
            self.executeRunList(self.result_queue.get())
