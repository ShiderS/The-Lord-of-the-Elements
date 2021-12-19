from textures import *
from hero import *
from level_characteristics import *
# from hero import *


level = 'level_1'


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Mygame')
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((66, 66, 61))

    pygame.display.flip()

    info_images = Level_characteristics(size[0], size[1], level).render()
    # берем из класса Levels местоположение текстурки и ее расположение на холсте
    for i in range(len(info_images[1])):
        fullname, x, y = Levels().return_level(info_images[0], info_images[1][i])
        # создаем спрайт
        textures = Textures(fullname, x, y)

    hero = Hero(textures)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hero.move_right()
                elif event.key == pygame.K_a:
                    hero.move_left()
                elif event.key == pygame.K_w:
                    hero.move_upp()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
        screen.fill((66, 66, 61))
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        all_sprites.update()
        all_sprites.draw(screen)
        hero_sprites.update()
        hero_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(144)