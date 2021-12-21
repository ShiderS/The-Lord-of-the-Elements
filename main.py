from textures import *
from hero import *
from level_characteristics import *
from radiation import *

# from hero import *


level = 'level_1'
list_textures = []
RIGHT = "right"
LEFT = "left"
STOP = "stop"

motion = STOP

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('The Lord of the Elements')
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
        list_textures.append(textures)

    hero = Hero(list_textures, size, screen)
    radiatoin = Radiation

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    motion = RIGHT
                if event.key == pygame.K_a:
                    motion = LEFT
                if event.key == pygame.K_w:
                    hero.move_upp()

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_a and motion == LEFT) or \
                        (event.key == pygame.K_d and motion == RIGHT):
                    motion = STOP

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos

        if motion == RIGHT:
            hero.move_right()
        elif motion == LEFT:
            hero.move_left()

        hp = hero.hp()
        x_hero, y_hero = hero.return_coords()

        screen.fill((66, 66, 61))

        pygame.draw.rect(screen, (255, 0, 0), (880, 20, hp, 20))
        if Radiation().dealing_damage(x_hero, y_hero) != None:
            hero.damage_fun(Radiation().dealing_damage(x_hero, y_hero))

        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)

        hero_sprites.update()
        hero_sprites.draw(screen)

        radiation_sprites.update()
        radiation_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(144)
