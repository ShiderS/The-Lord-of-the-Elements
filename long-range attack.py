import pygame
import sys, os

attack_sprites = pygame.sprite.Group()


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


class Long_Range_Attack(pygame.sprite.Sprite):
    def __init__(self, fullname, x, y):
        super().__init__(attack_sprites)

        self.image = load_image(fullname + '.png')
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y