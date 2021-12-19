import os


class Levels:
    def __init__(self):
        self.level_1 = []

    def return_level(self, number_of_elements, level, name):
        for i in range(number_of_elements):
            fullname = os.path.join('levels', level, 'images', name[i])
            x, y = 100, 100
            return fullname, x, y