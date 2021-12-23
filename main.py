from textures import *
from hero import *
from level_characteristics import *
from radiation import *

size = 1000, 800

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('The Lord of the Elements')
screen = pygame.display.set_mode(size)
screen.fill((66, 66, 61))

level = 'level_1'
list_textures = []
RIGHT = "right"
LEFT = "left"
STOP = "stop"

motion = STOP

isJump = False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - size[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - size[1] // 2)


camera = Camera()

if __name__ == '__main__':
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

        # # изменяем ракурс камеры
        # camera.update(hero)
        # # обновляем положение всех спрайтов
        # for sprite in all_sprites:
        #     camera.apply(sprite)

        if Radiation().dealing_damage(x_hero, y_hero) != None:
            hero.damage_fun(Radiation().dealing_damage(x_hero, y_hero))

        all_sprites.update()
        all_sprites.draw(screen)

        hero_sprites.update()
        hero_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(144)
