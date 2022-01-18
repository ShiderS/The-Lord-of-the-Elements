import pygame

attack_sprites = pygame.sprite.Group()


class Long_Range_Attack(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y,
                 list_textures, list_mobs, view):
        super().__init__(attack_sprites)

        self.counter = 0

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.list_textures = list_textures
        self.list_mobs = list_mobs
        self.view = view

    def cut_sheet(self, sheet, columns, rows):
        self.frames = []
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

        # if (not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures) or
        #     not any(pygame.sprite.collide_mask(self, i) for i in self.list_mobs)) and self.view == 'right':
        #     self.rect.x += 5
        # if (not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures) or
        #     not any(pygame.sprite.collide_mask(self, i) for i in self.list_mobs)) and self.view == 'left':
        #     self.rect.x -= 5

        if not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures) and self.view == 'right':
            self.rect.x += 5

        elif not any(pygame.sprite.collide_mask(self, i) for i in self.list_textures) and self.view == 'left':
            self.rect.x -= 5

        else:
            self.kill()
