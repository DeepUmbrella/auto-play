from threading import Thread
from typing import List, Tuple
import queue
import time

Prediction = Tuple[float, float, float, float, float, int]

# Define the type for the summary function's return value
Summary = List[Prediction]

role_id = "jianmo" # is your main role indecator , example: "role name" or "role id" and "some other info"
elite_monster_ids = ["monster1", "monster2", "monster3"] # is the monster id list
monsters_ids = ["monster4", "monster5", "monster6"] # is the monster id list

role_position = (0, 0) # is the role position

def calculate_bounding_box(predictions: List[Prediction]) -> Tuple[float, float, float,float]:
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
    def __init__(self, task_queue: queue.Queue):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.task_queue = task_queue

    def run(self):
        while True:
            result = self.task_queue.get()
            if result is None:
                break
            role_list = []
            elite_monster_list = []
            monster_list = []
            # monster bounding box
            role_bounding_box =None
            monster_bounding_box = []
            detect_result_summary:Summary = result.summary() # The summary function returns a list, each list item is an array containing x,y,x1,y1,confidence,classid

            for x, y, x1, y1, confidence, classid in detect_result_summary:
                if classid == role_id:
                    # filter all the role id equal to role_id and save to the role list
                    role_list.append([x, y, x1, y1, confidence, classid])
                    pass 
                if classid in elite_monster_ids:
                    # filter all the monster id equal to elite_monster_ids and save to the elite monster list
                    elite_monster_list.append([x, y, x1, y1, confidence, classid])
                    pass
                if classid in monsters_ids:
                    monster_list.append([x, y, x1, y1, confidence, classid])
                    # filter all the monster id equal to monsters_ids and save to the monster list
                    pass

            # calculate the role bounding box
            if len(role_list) > 0:
            
                role_bounding_box = calculate_bounding_box(role_list)
            # calculate the monster bounding box
            if monster_list:
                monster_bounding_box = calculate_bounding_box(monster_list)
                