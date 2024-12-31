from threading import Thread
from typing import List, Tuple
import cv2
import queue
import time

Prediction = Tuple[float, float, float, float, float, float]

# Define the type for the summary function's return value
Summary = List[Prediction]

# is your main role indecator , example: "role name" or "role id" and "some other info"
role_id = "jianmo"
elite_monster_ids = ["monster1", "monster2",
                     "monster3"]  # is the monster id list
monsters_ids = ["monster4", "monster5", "monster6"]  # is the monster id list

role_position = (0, 0)  # is the role position


def calculate_bounding_box(predictions: List[Prediction]) -> Tuple[float, float, float, float]:
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    for prediction in predictions:
        min_x = min(min_x, prediction[0])
        min_y = min(min_y, prediction[1])
        max_x = max(max_x, prediction[2])
        max_y = max(max_y, prediction[3])
    return min_x, min_y, max_x, max_y


class TaskCenter(Thread):
    def __init__(self, task_queue: queue.Queue, dev_model: bool = False):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.task_queue = task_queue
        self.dev_model = dev_model

    def run(self):
        while True:
            result = self.task_queue.get()

            detect_result_summary: Summary = result.summary()

            print(detect_result_summary)

            # if len(detect_result_summary) > 0:

            resultdemo = [
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.8346, 'box': {
                    'x1': 195.4014, 'y1': 118.48792, 'x2': 296.29547, 'y2': 263.31067}},
                {'name': 'xiazi', 'class': 17, 'confidence': 0.74028, 'box': {
                    'x1': 629.80243, 'y1': 138.47133, 'x2': 734.11621, 'y2': 283.63672}},
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.57023, 'box': {
                    'x1': 43.51778, 'y1': 369.18613, 'x2': 166.39531, 'y2': 502.31592}},
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.53187, 'box': {
                    'x1': 903.56238, 'y1': 361.32379, 'x2': 1026.4928, 'y2': 504.89212}},
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.51037, 'box': {
                    'x1': 619.75616, 'y1': 344.86658, 'x2': 715.93121, 'y2': 503.13309}},
                {'name': 'jianmo', 'class': 6, 'confidence': 0.49608, 'box': {
                    'x1': 45.27029, 'y1': 368.56796, 'x2': 164.02917, 'y2': 502.35999}},
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.32423, 'box': {
                    'x1': 313.75665, 'y1': 114.16856, 'x2': 451.42612, 'y2': 289.70303}},
                {'name': 'jianhun', 'class': 5, 'confidence': 0.32205, 'box': {
                    'x1': 324.47443, 'y1': 117.75164, 'x2': 449.24078, 'y2': 288.1795}},
                {'name': 'nvmanyou', 'class': 14, 'confidence': 0.30909, 'box': {
                    'x1': 487.46475, 'y1': 358.38928, 'x2': 569.45325, 'y2': 502.95258}},
                {'name': 'nanwuji', 'class': 12, 'confidence': 0.29574, 'box': {
                    'x1': 302.59952, 'y1': 113.62565, 'x2': 452.43298, 'y2': 291.08737}},
                {'name': 'jianmo', 'class': 6, 'confidence': 0.26233, 'box': {
                    'x1': 483.47418, 'y1': 145.87503, 'x2': 589.93323, 'y2': 262.88989}}
            ]

            img = result.plot().copy()
            boxes = result.boxes
            detected = len(boxes) != 0

            if detected:

                box = result.boxes[0]

                data = box.data

                data0 = data[0]

                data00 = data0.cpu().numpy()

                x1, y1, x2, y2, cof, cls = data00

                center_coordinates = (
                    int((x1 + x2) / 2), int((y1 + y2) / 2))

                x1, y1, x2, y2 = skill.calculate_area_coordinates(
                    center_coordinates[0], center_coordinates[1])
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

                print(x1, y1, x2, y2, cof, cls, 66666)
                if result is None:
                    break
                role_list = []
                elite_monster_list = []
                monster_list = []
                # monster bounding box
                role_bounding_box = None
                monster_bounding_box = None
                # The summary function returns a list, each list item is an array containing x,y,x1,y1,confidence,classid
                detect_result_summary: Summary = result.summary()

                for x, y, x1, y1, confidence, classid in detect_result_summary:
                    if classid == role_id:
                        # filter all the role id equal to role_id and save to the role list
                        role_list.append([x, y, x1, y1, confidence, classid])
                        pass
                    if classid in elite_monster_ids:
                        # filter all the monster id equal to elite_monster_ids and save to the elite monster list
                        elite_monster_list.append(
                            [x, y, x1, y1, confidence, classid])
                        pass
                    if classid in monsters_ids:
                        monster_list.append(
                            [x, y, x1, y1, confidence, classid])
                        # filter all the monster id equal to monsters_ids and save to the monster list
                        pass

                    # calculate the role bounding box
                if len(role_list) > 0:

                    role_bounding_box = calculate_bounding_box(role_list)
                    # calculate the monster bounding box
                if monster_list:
                    monster_bounding_box = calculate_bounding_box(
                        monster_list)

            if self.dev_model == True:
                if detected:
                    cv2.rectangle(img, (x1, y1),
                                  (x2, y2), (0, 255, 0), 2)
                cv2.imshow('predict', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
