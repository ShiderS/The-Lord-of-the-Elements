import pygame, os, sys


def load_image(name, colorkey=None):
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


class Map:
    stone_platform = load_image("stone_platform.png")
    wooden_platform = load_image('wooden_platform.png')

    # создание поля
    def __init__(self, width, height):
        self.matrix = []
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50

        # маска каменной платформы
        self.stone_platform = Map.stone_platform
        self.rect_stone_platform = self.stone_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.stone_platform)

        # маска деревянной платформы
        self.wooden_platform = Map.wooden_platform
        self.rect_wooden_platform= self.wooden_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_wooden_platform = pygame.mask.from_surface(self.wooden_platform)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for x in range(self.width):
            self.matrix.append([0 for i in range(self.height)])
        for x in range(self.width):
            for y in range(self.height):
                if self.matrix[x][y] == 0:
                    fill = (50, 50, 50)
                    stroke = (25, 25, 25)
                elif self.matrix[x][y] == 1:
                    self.rect_stone_platform.bottom = y
                    fill = (100, 100, 100)
                    stroke = (70, 70, 70)
                else:
                    self.rect_wooden_platform.bottom = y
                    fill = (0, 0, 0)
                    stroke = (0, 0, 0)
                pygame.draw.rect(screen, fill, ((self.left + self.cell_size * x,
                                                            self.top + self.cell_size * y),
                                                           (self.cell_size, self.cell_size)), 0)
                pygame.draw.rect(screen, stroke, ((self.left + self.cell_size * x,
                                                            self.top + self.cell_size * y),
                                                           (self.cell_size, self.cell_size)), 1)

    def click(self, x1, y1, screen):
        if x1 <= self.left + self.cell_size * self.width and y1 <= self.top + self.cell_size * self.height \
                and x1 >= self.left and y1 >= self.top:
            first_coord = (x1 - self.left) // self.cell_size
            second_coord = (y1 - self.top) // self.cell_size
            if self.matrix[first_coord][second_coord] == 0:
                self.matrix[first_coord][second_coord] = 1
            elif self.matrix[first_coord][second_coord] == 1:
                self.matrix[first_coord][second_coord] = 2
            else:
                self.matrix[first_coord][second_coord] = 0
            self.render(screen)
            return ''
        return None