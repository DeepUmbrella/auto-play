class Area():
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return f"{self.name} - {self.area}"

    def __repr__(self):
        return f"{self.name} - {self.area}"

    def __eq__(self, other):
        return self.name == other.name and self.area == other.area

    def __lt__(self, other):
        return self.area < other.area

    def __le__(self, other):
        return self.area <= other.area
