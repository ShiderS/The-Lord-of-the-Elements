import pygame
import os, sys

mobs_sprites = pygame.sprite.Group()


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


class Mob(pygame.sprite.Sprite):
    def __init__(self, image, coords, damage, hp,
                 list_textures, gravity, screen,
                 list_rect_textures, list_mask_textures, list_radiations,
                 list_attack, damage_attack, size):
        super().__init__(mobs_sprites)

        self.image = load_image(image)
        self.rect = self.image.get_rect()

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.wight = size[0]
        self.height = size[1]

        self.screen = screen

        self.list_textures = list_textures
        self.list_rect_textures = list_rect_textures
        self.list_mask_textures = list_mask_textures
        self.list_radiations = list_radiations
        self.list_attack = list_attack

        # вычисляем маску для эффективного сравнения
        self.mask_mob = pygame.mask.from_surface(self.image)

        self.movement_speed = 3
        self.jump_speed = 15
        self.dawn_speed = 5
        self.jump_height = 100
        self.gravity = gravity
        self.damage_attack = damage_attack

        self.damage = damage
        self.health = hp

    def update(self):
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect = self.rect.move(0, self.gravity)

        if any(pygame.sprite.collide_mask(self, i) for i in self.list_attack):
            self.health -= self.damage_attack

    def move_right(self):
        # offset = (self.rect.x - self.list_rect_textures[0].x, self.rect.y - self.list_rect_textures[0].y)
        # print(self.mask_hero.overlap_area(self.list_mask_textures[0], offset))
        # if any(self.mask_hero.overlap_area(mask_textures, offset) > 0 for mask_textures in self.list_mask_textures):
        #     pass
        if not any(rect_textures.collidepoint(self.rect.topright) for rect_textures in self.list_rect_textures):
            self.rect.x += self.movement_speed
        if self.rect.left > self.wight:
            self.rect.right = 0

    def move_left(self):
        if not any(rect_textures.collidepoint(self.rect.topleft) for rect_textures in self.list_rect_textures):
            self.rect.x -= self.movement_speed
        if self.rect.left < 0:
            self.rect.right = self.wight
        # self.cut_sheet(load_image("hero_left.png"), 4, 1)

    def move_upp(self, height_jump):
        if height_jump <= self.jump_height:
            self.rect.y -= self.jump_speed
        # if any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
        #     self.rect.y -= self.jump_height

    def move_dawn(self):
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect.y += self.dawn_speed

    def hp(self):
        return self.health

    def damage(self):
        self.health -= self.damage_attack