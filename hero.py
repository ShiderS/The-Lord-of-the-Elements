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


hero_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self, textures):
        super().__init__(hero_sprites)

        self.textures = textures

        # маска героя
        self.image = Hero.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.image)
        self.coord = self.x, self.y = 200, 0
        self.rect.x = self.x
        self.rect.y = self.y

        self.damage = 25
        self.health = 100

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, self.textures):
            self.rect = self.rect.move(0, 1)

    def move_right(self):
        self.rect.x += 5

    def move_left(self):
        self.rect.x -= 5

    def move_upp(self):
        self.rect.y -= 50