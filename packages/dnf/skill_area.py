

class Area():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def intersects(self, other):
        return not (self.x + self.width <= other.x or self.x >= other.x + other.width or
                    self.y + self.height <= other.y or self.y >= other.y + other.height)

    def area(self):
        return self.width * self.height

    def intersection_area(self, other):
        return Area(
            max(self.x, other.x),
            max(self.y, other.y),
            min(self.x + self.width, other.x +
                other.width) - max(self.x, other.x),
            min(self.y + self.height, other.y +
                other.height) - max(self.y, other.y)
        )

    def intersection_area_size(self, other):
        return self.intersection_area(other).area()

    def intersection_area_ratio(self, other):
        return self.intersection_area_size(other) / self.area() if self.area() > 0 else 0.0


class SkillArea(Area):
    def __init__(self, role_x, role_y, width, height, skill_):
        pass

    def __str__(self):
        pass
