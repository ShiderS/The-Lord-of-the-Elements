from textures import *
# from hero import *


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    pygame.display.set_caption('Mygame')
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((66, 66, 61))

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
        screen.fill((66, 66, 61))
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(144)