import pygame
from Map import *
from hero import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Mygame')
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('Black'))
    pygame.display.flip()
    board = Map(19, 15)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                board.click(x1, y1, screen)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
