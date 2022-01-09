from level_characteristics import *
from radiation import *
from Particle import *

size = 1000, 800
screen_rect = (0, 0, size[0], size[1])

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
height_jump = 0
number_of_jumps = 0
max_number_of_jumps = 1
flag_jump = False


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
        self.movement_speed = 3
        self.jump_speed = 10
        self.jump_height = 100

    # сдвинуть объект obj на смещение камеры
    def apply_upp(self, obj):
        # obj.rect.x += self.dx
        obj.rect.y += self.jump_height

    def apply_left(self, obj):
        obj.rect.x += self.movement_speed

    def apply_right(self, obj):
        obj.rect.x -= self.movement_speed

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - size[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - size[1] // 2)


camera = Camera()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


if __name__ == '__main__':
    # start_screen()
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
    rect_hero = hero.return_rect()

    running = True

    # изменяем ракурс камеры
    camera.update(hero)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    motion = RIGHT
                if event.key == pygame.K_a:
                    motion = LEFT
                if event.key == pygame.K_w:
                    isJump = True
                    number_of_jumps += 1

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_a and motion == LEFT) or \
                        (event.key == pygame.K_d and motion == RIGHT):
                    motion = STOP
                if event.key == pygame.K_w:
                    isJump = False
                    height_jump = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos

        if motion == RIGHT:
            hero.move_right()
            # if not any(rect_textures.collidepoint(rect_hero.topright) for rect_textures in list_rect_textures):
            for sprite in all_sprites:
                camera.apply_right(sprite)
        if motion == LEFT:
            hero.move_left()
            for sprite in all_sprites:
                camera.apply_left(sprite)
        if isJump and number_of_jumps <= max_number_of_jumps:
            height_jump += 10
            hero.move_upp(height_jump)

        hp = hero.hp()
        x_hero, y_hero = hero.return_coords()

        if hp <= 0 or y_hero >= 800:
            hp = 0
            hero.kill()

        screen.fill((66, 66, 61))

        if hp > 0:
            pygame.draw.rect(screen, (255, 0, 0), (880, 20, hp, 20))

        flag_jump = hero.return_flag_jump()

        if flag_jump:
            number_of_jumps = 0

        all_sprites.update()
        all_sprites.draw(screen)

        hero_sprites.update()
        hero_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)
