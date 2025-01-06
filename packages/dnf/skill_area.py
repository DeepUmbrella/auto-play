class Skill:
    def __init__(self, id, range, release_quick_keyboard='x', composition_keyboards='', cool_time=0, level=0):
        self.id = id
        self.cool_time = cool_time
        self.level = level
        self.range = range
        self.release_able = True
        self.last_release_time = 0
        self.release_quick_keyboard = release_quick_keyboard
        self.composition_keyboards = composition_keyboards

    def release_skill(self):
        if not self.release_able:
            return

        self.last_release_time = self.current_time()
        self.release_able = False
        # Start timing

        # Until timing ends

    def check_and_set_release_status(self):
        current_time = self.current_time()
        executed_time = current_time - self.last_release_time
        if executed_time >= self.cool_time:
            self.release_able = True

    @staticmethod
    def current_time():
        import time
        return int(time.time())


def calculate_best_skill(skill_list, pos):
    best_skill_id = 'normal'
    best_intersection_rate = 0
    best_skill_index = 0

    x, y, width, height = pos

    for index, skill in enumerate(skill_list):
        skill.check_and_set_release_status()

        if not skill.release_able:
            continue

        skill_width, skill_height = skill.range
        intersect_area = min(skill_width, width) * min(height, skill_height)
        intersection_rate = round(intersect_area / (width * height), 1)

        if best_intersection_rate < intersection_rate:
            best_intersection_rate = intersection_rate
            best_skill_id = skill.id
            best_skill_index = index

    return best_skill_index


# Example of initData for context
