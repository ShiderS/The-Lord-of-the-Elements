import pygame

hero_sprites = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, list_textures, gravity,
                 list_rect_textures, list_mask_textures, list_radiations, size, screen):
        super().__init__(hero_sprites)

        self.list_textures = list_textures
        self.list_rect_textures = list_rect_textures
        self.list_mask_textures = list_mask_textures
        self.list_radiations = list_radiations

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
        self.mask_hero = pygame.mask.from_surface(self.image)

        self.coord = self.x, self.y = 200, 0
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_speed = 3
        self.jump_speed = 15
        self.dawn_speed = 5
        self.jump_height = 100
        self.gravity = gravity

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
            self.rect = self.rect.move(0, self.gravity)
        if any(pygame.sprite.collide_mask(self, i) for i in self.list_radiations):
            self.damage_fun(0.1)

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

    def move_upp(self, height_jump):
        if height_jump <= self.jump_height:
            self.rect.y -= self.jump_speed
        # if any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
        #     self.rect.y -= self.jump_height

    def move_dawn(self):
        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures):
            self.rect.y += self.dawn_speed

    def damage_fun(self, damage):
        if self.health > 0:
            self.health -= damage
        else:
            self.kill()

    def hp(self):
        return self.health

    def return_coords(self):
        return self.rect.x, self.rect.y

    def return_rect(self):
        return self.rect

    def return_flag_jump(self):
        return any(pygame.sprite.collide_mask(self, i) for i in self.list_textures)

    def return_flag_move_left(self):
        return any(rect_textures.collidepoint(self.rect.topleft) for rect_textures in self.list_rect_textures)

    def return_flag_move_right(self):
        return any(rect_textures.collidepoint(self.rect.topright) for rect_textures in self.list_rect_textures)
