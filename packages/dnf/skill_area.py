class Skill():
    def __init__(self, width, height, x_offset=0, cooling_time=5, release_time=1, skill_level=0):
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.cooling_time = cooling_time
        self.release_time = release_time
        self.skill_level = skill_level

        pass

    def calculate_area_coordinates(self, role_x, role_y, direction="right"):

        indicator = 1 if direction == 'right' else -1
        x1 = role_x + (0 * indicator)
        y1 = role_y - self.height/2
        x2 = x1 + (self.width * indicator)
        y2 = y1 + self.height

        return x1, y1, x2, y2

    def contains(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def intersects(self, other):
        return not (self.x + self.width <= other.x or self.x >= other.x + other.width or
                    self.y + self.height <= other.y or self.y >= other.y + other.height)

    def area(self):
        return self.width * self.height

    def intersection_area_size(self, other):
        return self.intersection_area(other).area()

    def intersection_area_ratio(self, other):
        return self.intersection_area_size(other) / self.area() if self.area() > 0 else 0.0
