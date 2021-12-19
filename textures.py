import pygame, sys
from levels import *
from Map import *

# настройки дисплея
size = 1000, 800
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()

info = Map(size[0], size[1]).render()
# берем из класса Levels местоположение текстурки и ее расположение на холсте
fullname, x, y = Levels().return_level(*info)


# загрузка изображения
def load_image(fullname, colorkey=None):
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


# отображение текстуры
class Textures(pygame.sprite.Sprite):
    stone_platform = load_image(fullname)

    def __init__(self, x, y):
        super().__init__(all_sprites)

        # маска каменной платформы
        self.image = Textures.stone_platform
        self.rect = self.stone_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y