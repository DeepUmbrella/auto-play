from threading import Thread
from queue import Queue
from typing import List, Callable, Any
from .object_type import Single, Multi, ObjectType
from collections import defaultdict
from typing import TypedDict, Dict, List


class Box(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float


class Result(TypedDict):
    name: str
    confidence: float
    box: Box
    class_: int


def get_object_type_by_id(id: int) -> ObjectType:

    if id in Single:
        return ObjectType.SINGLE
    elif id in Multi:
        return ObjectType.MULTI
    else:
        return ObjectType.UNKNOWN


def getSummary(result, *args) -> List[Result]:

    return result.summary(decimals=2)


def filterConfidence(result: list, *args) -> List[Result]:
    return sorted([r for r in result if r['confidence'] > 0.5], key=lambda x: x['confidence'], reverse=True)


def sendEvent():
    pass


def classification_by_class(result: list, *args) -> Dict[int, List[Box]]:
    result_dict: Dict[int, List[Box]] = defaultdict(list)
    for r in result:
        result_dict[r['class']].append(r["box"])
    return result_dict


def get_same_class_big_box(result: Dict[int, List[Box]], *args) -> Dict[int, Box]:
    empty_dict: Dict[int, Box] = {}
    for k, v in result.items():
        if len(v) < 1:
            continue

        obj_type = get_object_type_by_id(k)

        if obj_type == ObjectType.SINGLE:
            empty_dict[k] = v[0]
        else:
            x1 = min([b['x1'] for b in v])
            y1 = min([b['y1'] for b in v])
            x2 = max([b['x2'] for b in v])
            y2 = max([b['y2'] for b in v])
            empty_dict[k] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

    return empty_dict


run_list: List[Callable[..., Any]] = [
    getSummary,
    filterConfidence,
    classification_by_class,
    get_same_class_big_box,
]


class TaskCenter(Thread):
    def __init__(self, result_queue: Queue):
        super().__init__()
        self.name = f'Worker-{id(self)}'
        self.daemon = True
        self.result_queue = result_queue
        self.run_list = run_list

    def executeRunList(self, practice_result, *args):
        pre_input = practice_result
        for func in run_list:
            if callable(func):
                pre_input = func(pre_input, practice_result, *args)
        pass

    def run(self):
        if len(self.run_list) == 0 or self.run_list is None:
            print("No task to run, exit")
            return

        while True:
            result, img_source = self.result_queue.get()
            self.executeRunList(result)
