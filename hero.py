import pygame

hero_sprites = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, list_textures, size, screen):
        super().__init__(hero_sprites)

        self.list_textures = list_textures

        self.counter = 0

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.wight = size[0]
        self.height = size[1]
        self.screen = screen

        # маска героя
        # self.image = Hero.image
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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.counter == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.counter = 0
        else:
            self.counter += 1
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