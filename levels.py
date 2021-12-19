import os


class Levels:
    def __init__(self):
        self.level_1 = []

    def return_level(self, level, name):
        fullname = os.path.join('levels', level, 'images', name)
        file_open = open(os.path.join('levels', level, 'coords', name[:-4] + '_coords.txt')
                         , encoding='utf8').read().splitlines()
        x, y = file_open[0].split()
        x, y = int(x), int(y)
        return fullname, x, y