class Level_characteristics:
    # создание поля
    def __init__(self, width, height):
        self.matrix = []
        self.width = width
        self.height = height
        # self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию

    def render(self):
        number_of_elements, level, names = 2, 'level_1', ['stone_platform.png', 'wooden_platform.png']
        return number_of_elements, level, names