

from utils.screen_capture import ScreenCapture
from utils.predict import Predict
import queue
import threading


if __name__ == '__main__':
    MAX_QUEUE_SIZE = 60
    stop_signal = threading.Event()
    img_queue = queue.Queue(MAX_QUEUE_SIZE)
    screen_capture = ScreenCapture()
    predictor = Predict(img_queue)
    producer_thread = threading.Thread(
        target=screen_capture.producer, args=(img_queue, stop_signal))
    # consumer_thread = threading.Thread(
    #     target=predictor.consumer, args=(img_queue, stop_signal, True))
    producer_thread.start()
    predictor.consumer(img_queue, stop_signal)
    # consumer_thread.start()

    # producer_thread.join()
    # consumer_thread.join()
