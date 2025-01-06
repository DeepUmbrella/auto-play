from typing import List, Tuple, TypedDict


class BoundingBox(TypedDict):
    x1: float
    x2: float
    y1: float
    y2: float


class Result(TypedDict):
    __annotations__ = {
        'class': int  # 使用 __annotations__ 来定义 class 键
    }
    name: str
    box: BoundingBox
    confidence: float


Position = Tuple[float, float, float, float]

Summary = List[Result]
