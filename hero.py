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


class Hero(pygame.sprite.Sprite):
    image = load_image("hero.png")

    def __init__(self, list_textures, size, screen):
        super().__init__(hero_sprites)

        self.list_textures = list_textures

        self.wight = size[0]
        self.height = size[1]
        self.screen = screen

        # маска героя
        self.image = Hero.image
        self.rect = self.image.get_rect()

        # вычисляем маску для эффективного сравнения
        self.mask_stone_platform = pygame.mask.from_surface(self.image)

        self.coord = self.x, self.y = 200, 0
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_speed = 2
        self.jump_speed = 10
        self.jump_height = 150

        self.damage = 25
        self.health = 100

    def update(self):
        # если ещё в небе
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect = self.rect.move(0, 2)

    def move_right(self):
        self.rect.x += self.movement_speed
        if self.rect.left > self.wight:
            self.rect.right = 0

    def move_left(self):
        self.rect.x -= self.movement_speed
        if self.rect.left < 0:
            self.rect.right = self.wight

    def move_upp(self):
        if any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect.y -= self.jump_height

    def damage_fun(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.kill()

    def hp(self):
        return self.health

    def return_coords(self):
        return self.rect.x, self.rect.y