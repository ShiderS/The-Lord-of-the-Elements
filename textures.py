import pygame, sys, os

# настройки дисплея
size = 1000, 800
screen = pygame.display.set_mode(size)

# спрайты
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


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
    # image = load_image(fullname)

    def __init__(self, fullname, x, y):
        super().__init__(all_sprites)

        # маска каменной платформы
        # self.image = Textures.image
        self.image = load_image(fullname)
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def get_rect(self):
        return self.rect

    def get_mask(self):
        return self.mask