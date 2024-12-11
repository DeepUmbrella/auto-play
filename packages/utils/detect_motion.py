import cv2


def detect_motion(previous_frame, current_frame):
    diff = cv2.absdiff(previous_frame, current_frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 25, 255, cv2.THRESH_BINARY)
    motion_contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return motion_contours
