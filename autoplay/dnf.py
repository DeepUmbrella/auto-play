
import pywinctl as gw
from PIL import ImageGrab
import cv2
import numpy as np
import ffmpeg
import subprocess
import mss
import time

from utils.screen_capture import ScreenCapture


def get_window_bbox(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        raise Exception(f"Window with title '{window_title}' not found.")
    window = windows[0]
    bbox = (window.left, window.top, window.right, window.bottom)
    return bbox


def capture_window(window_title, output_url, fps=30):

    cap = ScreenCapture(top=100, left=100, width=800, height=600
                        )
    cap.set_size(top=240, left=560, width=800, height=600)
    cap.capture_window(dev=True)

    print(gw.getAllTitles(), gw.getAllWindows(),
          np.array([[1, 2], [3, 4], [5, 6]]))

# bbox = get_window_bbox(window_title)

# FFmpeg推流命令
# command = [
#     'ffmpeg',
#     '-y',
#     '-f', 'rawvideo',1
#     '-vcodec', 'rawvideo',
#     '-pix_fmt', 'bgr24',
#     '-s', f"{bbox[2] - bbox[0]}x{bbox[3] - bbox[1]}",
#     '-r', str(fps),
#     '-i', '-',
#     '-c:v', 'libx264',
#     '-preset', 'fast',
#     '-f', 'flv',
#     output_url
# ]

# process = subprocess.Popen(command, stdin=subprocess.PIPE)

# try:
#     while True:
#         img = ImageGrab.grab(bbox=bbox)  # 捕获窗口画面
#         img_np = np.array(img)  # 转换为NumPy数组
#         img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # 转换为BGR格式
#         # process.stdin.write(img_bgr.tobytes())  # 将图像写入FFmpeg进程
# except KeyboardInterrupt:
#     print("Streaming stopped.")
# finally:
#     process.stdin.close()
#     process.wait()


if __name__ == '__main__':
    window_title = "Google Chrome"  # 替换为你要捕获的窗口标题
    output_url = "rtmp://localhost:8080/live/ffmpeg"  # 替换为你的流媒体服务器URL
    capture_window(window_title, output_url)
