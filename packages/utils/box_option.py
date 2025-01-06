from typing import List
from .utils_typing import BoundingBox, Position, Summary


def get_xywh(box: BoundingBox) -> Position:
    x1, x2, y1, y2 = box['x1'], box['x2'], box['y1'], box['y2']
    return x1, y1, x2 - x1, y2 - y1


def get_collection_box(name_array: List[str], results: Summary) -> Position:
    if not results:
        return 0, 0, 0, 0

    left = results[0]['box']['x1']
    top = results[0]['box']['y1']
    max_left = 0
    max_top = 0

    for item in results:
        if item['name'] in name_array:
            left = min(left, item['box']['x1'])
            top = min(top, item['box']['y1'])
            max_left = max(max_left, item['box']['x2'])
            max_top = max(max_top, item['box']['y2'])

    return left, top, max_left - left, max_top - top
