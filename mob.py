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
                 list_attack, damage_attack, size, view_mob, mob_see):
        super().__init__(mobs_sprites)

        self.RIGHT = "right"
        self.LEFT = "left"
        self.STOP = "stop"

        self.image = load_image(image)
        self.rect = self.image.get_rect()

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.wight = size[0]
        self.height = size[1]
        self.move = self.STOP

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

        self.view_mob = view_mob
        self.mob_see = mob_see

    def update(self):
        if self.move == self.RIGHT:
            self.move_right()
        if self.move == self.LEFT:
            self.move_left()
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect = self.rect.move(0, self.gravity)

        if any(pygame.sprite.collide_mask(self, i) for i in self.list_attack):
            self.health -= self.damage_attack
        if any(pygame.sprite.collide_mask(self, i) for i in self.list_radiations):
            self.damage_fun(0.2)

    def move_right(self):
        if any(rect_textures.collidepoint(self.rect.topright) for rect_textures in self.list_rect_textures):
            self.rect.x += self.movement_speed

    def move_left(self):
        if any(rect_textures.collidepoint(self.rect.topleft) for rect_textures in self.list_rect_textures):
            self.rect.x -= self.movement_speed
        # self.cut_sheet(load_image("hero_left.png"), 4, 1)

    def move_upp(self, height_jump):
        if height_jump <= self.jump_height:
            self.rect.y -= self.jump_speed
        # if any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
        #     self.rect.y -= self.jump_height

    def move_dawn(self):
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect.y += self.dawn_speed

    def change_move(self, move):
        self.move = move

    def hp(self):
        return self.health

    def damage(self):
        self.health -= self.damage_attack

    def return_coords(self):
        return self.rect.x, self.rect.y

    def damage_fun(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.kill()

    def mob_see(self):
        self.flag_attack = True

    def mob_not_see(self):
        self.flag_attack = False

    def change_view(self, view_mob):
        self.view_mob = view_mob