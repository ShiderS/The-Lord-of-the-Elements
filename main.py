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
list_radiations = []
list_rect_textures = []
list_mask_textures = []
RIGHT = "right"
LEFT = "left"
STOP = "stop"
counter = 0

motion = STOP

isJump = False


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


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
    info_images = Level_characteristics(size[0], size[1], level, 'info_level.txt').render()
    info_images_radiation = Level_characteristics(size[0], size[1], level, 'info_radiation.txt').render()

    # берем из класса Levels местоположение текстурки и ее расположение на холсте
    for i in range(len(info_images[1])):
        fullname, x, y = Levels().return_level(info_images[0], info_images[1][i], 'images')
        # создаем спрайт
        textures = Textures(fullname, x, y)
        rect = Textures(fullname, x, y).get_rect()
        mask = Textures(fullname, x, y).get_mask()
        list_textures.append(textures)
        list_rect_textures.append(rect)
        list_mask_textures.append(mask)

    for i in range(len(info_images_radiation[1])):
        fullname, x, y = Levels().return_level(info_images_radiation[0], info_images_radiation[1][i], 'radiations')
        # создаем спрайт
        radiation = Radiation(fullname, (x, y))
        list_radiations.append(radiation)

    hero = Hero(load_image("hero_.png"), 4, 1, list_textures, list_rect_textures, list_mask_textures, list_radiations, size, screen)

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

        if hp <= 0 or y_hero >= 800:
            hp = 0
            hero.kill()

        screen.fill((66, 66, 61))

        if hp > 0:
            pygame.draw.rect(screen, (255, 0, 0), (880, 20, hp, 20))

        # # изменяем ракурс камеры
        # camera.update(hero)
        # # обновляем положение всех спрайтов
        # for sprite in all_sprites:
        #     camera.apply(sprite)

        all_sprites.update()
        all_sprites.draw(screen)

        hero_sprites.update()
        hero_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)
