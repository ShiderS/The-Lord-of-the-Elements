import pygame, os, sys


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


class Hero(pygame.sprite.Sprite):
    image = load_image("pers.png")

    def __init__(self):
        super().__init__(all_sprites)

        # маска героя
        self.image = Hero.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.image)
        self.coord = self.x, self.y = 500, 400
        self.rect.x = self.x
        self.rect.y = self.y
        self.damage = 25
        self.health = 100

    def movement(self):
        if self.x >= 0:
            if key:
                self.x += 1
            if key:
                self.x -= 1
            if key:
                self.y += 1