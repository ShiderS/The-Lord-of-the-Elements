import pygame

mobs_sprites = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, count_mobs):
        super().__init__()

        self.count_mobs = count_mobs

    def update(self):
        pass

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
