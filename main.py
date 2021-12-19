import pygame
from textures import *
# from hero import *


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    pygame.display.set_caption('Mygame')
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('White'))

    pygame.display.flip()
    board = Textures(x, y)
    # hero = Hero()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(144)