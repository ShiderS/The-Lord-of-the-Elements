class Level_characteristics:
    # создание поля
    def __init__(self, width, height, level, info):
        self.matrix = []
        self.width = width
        self.height = height
        self.level = level
        self.info = info

    def render(self):
        file_open = open(f'levels\{self.level}\{self.info}', encoding='utf8').read().splitlines()
        names = file_open[0].split()
        return self.level, names