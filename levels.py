import os


class Levels:
    def __init__(self):
        self.level_1 = []

    def return_level(self, level, name, info):
        fullname = os.path.join('levels', level, info, name)
        x, y = name.split('x')
        x, y = int(x), int(y)
        return fullname, x, y