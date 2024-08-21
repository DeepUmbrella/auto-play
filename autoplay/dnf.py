

from PIL import ImageGrab
import cv2
import numpy as np

import subprocess
import mss
import time

from utils.screen_capture import ScreenCapture


def capture_window(window_title, output_url, fps=30):

    command = [
        'ffmpeg',
        '-re',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "800x600",
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryfast',
        '-f', 'flv',
        output_url,
    ]

    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE)

        cap = ScreenCapture()
        cap.set_size(top=240, left=560, width=800, height=600)
        cap.capture_window(dev=True, output=process.stdin.write)

    except KeyboardInterrupt:
        print("Streaming stopped.")
    finally:
        try:
            process.stdin.close()
            process.wait()
        except Exception as e:
            print(f"Failed to close process: {e}")


if __name__ == '__main__':
    window_title = "Google Chrome"  # 替换为你要捕获的窗口标题
    output_url = "rtmp://localhost:1935/live/ffmpeg"  # 替换为你的流媒体服务器URL
    # output_url = "output.mp4"  # 替换为你的流媒体服务器URL
    capture_window(window_title, output_url)
