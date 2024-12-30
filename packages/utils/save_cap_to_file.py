
import os
from threading import Thread
import time
import cv2
from queue import Queue, Empty


class SaveCapToFile(Thread):
    def __init__(self, source_queue: Queue,
                 file_name: str,
                 folder_path: str = None,
                 daemon=True):
        super().__init__()
        self.file_name = file_name
        self.folder_path = folder_path
        self.source_queue = source_queue
        self.daemon = daemon

    def run(self):
        folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        folder_path = "" if folder_path is None else folder_path

        while True:
            try:
                img = self.source_queue.get()
            except Empty:
                print("Queue is empty for 10 seconds. Exiting...")
                break

            # 生成文件名并保存图像
            timestamp = int(time.time() * 1000)
            img_name = f"frame_{timestamp}_{self.file_name}"
            filename = os.path.join(folder_path, img_name)
            cv2.imwrite(filename, img)
