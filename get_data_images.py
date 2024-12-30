from packages.utils import ScreenCapture, ScreenMatch, SaveCapToFile
from queue import Queue


if __name__ == '__main__':

    screen_match = ScreenMatch("地下城与勇士")
    start_save = False
    save_capture_queue = Queue()

    def capture_callback(img):
        if start_save:
            save_capture_queue.put(img)
        pass

    def onPressedKey(key):
        global start_save
        if key == ord('s'):
            start_save = not start_save
        pass

    screen_capture = ScreenCapture(
        capture_size=screen_match.size,
        capture_callback=capture_callback,
        pressed_key=onPressedKey,
        fps=3,
        dev_model=True)

    SaveCapToFile(
        source_queue=save_capture_queue,
        file_name="dnf.png",
        folder_path="data/images",
    ).start()
    screen_capture.start()
    screen_capture.join()
