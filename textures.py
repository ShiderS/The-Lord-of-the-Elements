import pygame, os, sys


size = 1000, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
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


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Stone_Textures(pygame.sprite.Sprite):
    stone_platform = load_image("stone_platform.png")
    # wooden_platform = load_image('wooden_platform.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)

        # маска деревянной платформы
        # self.wooden_platform = Textures.wooden_platform
        # self.rect_wooden_platform = self.wooden_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        # self.mask_wooden_platform = pygame.mask.from_surface(self.wooden_platform)

        # маска каменной платформы
        self.image = Stone_Textures.stone_platform
        self.rect = self.stone_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.image)
        self.rect.x = x * 50
        self.rect.y = y * 50


class Wooden_Textures(pygame.sprite.Sprite):
    wooden_platform = load_image('wooden_platform.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)

        # маска деревянной платформы
        self.image = Wooden_Textures.wooden_platform
        self.rect = self.wooden_platform.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_wooden_platform = pygame.mask.from_surface(self.image)

        self.rect.x = x * 50
        self.rect.y = y * 50