from Particle import *
from radiation import *
from attack import *
from mob import *
from mob_attack import *
import os, sys
import random
from threading import Thread

size = 1000, 800
screen_rect = (0, 0, size[0], size[1])

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('The Lord of the Elements')
screen = pygame.display.set_mode(size)
screen.fill((66, 66, 61))
screen.set_alpha(None)

list_textures = []
list_radiations = []
list_mobs = []
list_attack = []
list_rect_textures = []
list_mask_textures = []
list_mob_attack = []
list_mob_timer = []

RIGHT = "right"
LEFT = "left"
STOP = "stop"
list_move_mobs = [RIGHT, LEFT, STOP]
list_move_all_mobs = []
gravity = 5
jump_height = 100
view = RIGHT

level = 'level_2'
count_mobs = 1
damage_attack = 15
damage_attack_mob = 5


# isJump = False
# isDawn = False
# height_jump = 0
# number_of_jumps = 0
# max_number_of_jumps = 2
# flag_jump = False


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
        self.jump_speed = 15
        self.jump_height = 100

    # сдвинуть объект obj на смещение камеры
    def apply_upp(self, obj):
        # obj.rect.x += self.dx
        obj.rect.y += self.jump_speed

    def apply_dawn(self, obj):
        obj.rect.y -= self.jump_speed

    def apply_left(self, obj):
        if not hero.return_flag_move_left():
            obj.rect.x += self.movement_speed

    def apply_right(self, obj):
        if not hero.return_flag_move_right():
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
    # intro_text = ["ЗАСТАВКА", "",
    #               "Правила игры",
    #               "Если в правилах несколько строк,",
    #               "приходится выводить их построчно"]

    start_button = pygame.draw.rect(screen, (0, 0, 240), (300, 190, 400, 80))
    continue_button = pygame.draw.rect(screen, (0, 244, 0), (300, 340, 400, 80))
    quit_button = pygame.draw.rect(screen, (244, 0, 0), (300, 490, 400, 80))

    fon = pygame.transform.scale(load_image('fon.png'), size)

    screen.blit(fon, (0, 0))

    # font = pygame.font.Font(None, 30)
    # text_coord = 50

    # for line in intro_text:
    #     string_rendered = font.render(line, 1, pygame.Color('white'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 10
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def clear_map():
    pass


def continue_level():
    start_button = pygame.draw.rect(screen, (0, 0, 240), (300, 190, 400, 80))
    continue_button = pygame.draw.rect(screen, (0, 244, 0), (300, 340, 400, 80))
    quit_button = pygame.draw.rect(screen, (244, 0, 0), (300, 490, 400, 80))


def start_level():
    mobs_timer = 0
    mobs_attack_timer = 0
    motion = STOP

    isJump = False
    isDawn = False
    height_jump = 0
    number_of_jumps = 0
    max_number_of_jumps = 2

    view = RIGHT
    view_mob = RIGHT
    mob_see = False
    list_mobs = []

    # start_screen()

    # берем из класса Levels местоположение текстурки и ее расположение на холсте
    os.chdir('levels/' + level + '/images')
    for i in os.listdir():
        if 'x' in i:
            x, y = (int(j) for j in i[:-4].split('x'))
            fullname = os.path.abspath(i)
            textures = Textures(fullname, x, y)
            rect = Textures(fullname, x, y).get_rect()
            mask = Textures(fullname, x, y).get_mask()
            list_textures.append(textures)
            list_rect_textures.append(rect)
            list_mask_textures.append(mask)

    os.chdir('../radiations')

    for i in os.listdir():
        if 'x' in i:
            x, y = (int(j) for j in i[:-4].split('x'))
            fullname = os.path.abspath(i)
            # создаем спрайт
            radiation = Radiation(fullname, (x, y))
            list_radiations.append(radiation)

    os.chdir('../mobs')

    for i in os.listdir():
        if 'x' in i:
            x, y = (int(j) for j in i[:-4].split()[0].split('x'))
            damage = int(i[:-4].split()[2])
            hp = int(i[:-4].split()[1])
            fullname = os.path.abspath(i)
            mob = Mob(fullname, (x, y), damage, hp, list_textures, gravity, screen,
                      list_rect_textures, list_mask_textures, list_radiations, list_attack,
                      damage_attack, size, view_mob, mob_see)
            list_mobs.append(mob)
            list_mob_timer.append(0)
    os.chdir('../../..')

    rect_hero = hero.return_rect()

    running_level = True

    # изменяем ракурс камеры
    camera.update(hero)

    while running_level:
        x_hero, y_hero = hero.return_coords()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_level = False
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    motion = RIGHT
                    view = RIGHT
                    hero.give_animation(load_image("hero_right.png"), 4, 1, x_hero, y_hero)
                if event.key == pygame.K_a:
                    motion = LEFT
                    view = LEFT
                    hero.give_animation(load_image("hero_left.png"), 4, 1, x_hero, y_hero)
                if event.key == pygame.K_w:
                    isJump = True
                    number_of_jumps += 1
                if event.key == pygame.K_s:
                    isDawn = True

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_a and motion == LEFT) or \
                        (event.key == pygame.K_d and motion == RIGHT):
                    motion = STOP
                if event.key == pygame.K_w:
                    isJump = False
                    height_jump = 0
                if event.key == pygame.K_s:
                    isDawn = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    attack = Long_Range_Attack(load_image('long_range_attacke_animation.png'),
                                               4, 1, x_hero + 10, y_hero + 20, list_textures, list_mobs, view,
                                               damage_attack)
                    list_attack.append(attack)

        counter_mob_timer = 0
        for i in mobs_sprites:
            rand = random.randint(0, 2)
            move_mob = list_move_mobs[rand]
            if list_mob_timer[counter_mob_timer] == 25:
                i.change_move(move_mob)
                list_mob_timer[counter_mob_timer] = 0
            else:
                list_mob_timer[counter_mob_timer] += 1
            counter_mob_timer += 1

        if motion == RIGHT:
            hero.move_right()
            for sprite in all_sprites:
                camera.apply_right(sprite)
            for sprite in mobs_sprites:
                camera.apply_right(sprite)
            for sprite in attack_sprites:
                camera.apply_right(sprite)
        if motion == LEFT:
            hero.move_left()
            for sprite in all_sprites:
                camera.apply_left(sprite)
            for sprite in mobs_sprites:
                camera.apply_left(sprite)
            for sprite in attack_sprites:
                camera.apply_left(sprite)
        if isJump and number_of_jumps <= max_number_of_jumps:
            height_jump += 10
            hero.move_upp(height_jump)
            # for sprite in all_sprites:
            #     camera.apply_upp(sprite)
        if isDawn:
            hero.move_dawn()

        hp = hero.hp()

        screen.fill((66, 66, 61))

        if hp <= 0 or y_hero >= 800:
            hp = 0
            hero.kill()
            for i in list_attack:
                i.kill()
            pygame.display.flip()
            continue_level()
            running_level = False

        for i in range(len(list_mobs)):
            x_mob, y_mob = list_mobs[i].return_coords()
            hp_mob = list_mobs[i].hp()
            if -400 <= x_mob - x_hero <= 300:
                list_mobs[i].change_move(STOP)
                if 10 <= x_mob - x_hero <= 300:
                    list_mobs[i].move_left()
                    list_mobs[i].change_view(LEFT)
                    list_mobs[i].change_move(STOP)
                    if mobs_attack_timer < 50:
                        mobs_attack_timer += 1
                    else:
                        mob_attack = Attack_Mob(load_image('long_range_attacke_animation.png'),
                                                4, 1, x_mob + 10, y_mob + 20, list_textures,
                                                hero, damage_attack, list_mobs[i].return_view())
                        list_mob_attack.append(mob_attack)
                        mobs_attack_timer = 0
                if -300 <= x_mob - x_hero <= -10:
                    list_mobs[i].move_right()
                    list_mobs[i].change_view(RIGHT)
                    list_mobs[i].change_move(STOP)
                    if mobs_attack_timer < 50:
                        mobs_attack_timer += 1
                    else:
                        mob_attack = Attack_Mob(load_image('long_range_attacke_animation.png'),
                                                4, 1, x_mob + 10, y_mob + 20, list_textures,
                                                hero, damage_attack, list_mobs[i].return_view())
                        list_mob_attack.append(mob_attack)
                        mobs_attack_timer = 0
            if list_mobs[i].hp() <= 0 or y_mob >= 800:
                list_mobs[i].kill()
                del list_mobs[i]
                break
            else:
                pygame.draw.rect(screen, (255, 0, 0), (x_mob, y_mob, hp_mob, 10))

        for i in range(len(list_attack)):
            # x_attack, y_attack = list_attack[i].return_coords()
            if list_attack[i].flag_attack():
                del list_attack[i]
                break
            # elif x_attack > 1000 or x_attack < 0:
            #     del list_attack[i]
            #     break
        for i in range(len(list_mob_attack)):
            # x_mob_attack, y_mob_attack = list_attack[i].return_coords()
            if list_mob_attack[i].flag_attack():
                del list_mob_attack[i]
                break
            # elif x_mob_attack > 1000 or x_mob_attack < 0:
            #     del list_mob_attack[i]
            #     break

        if hp > 0:
            pygame.draw.rect(screen, (255, 0, 0), (880, 20, hp, 20))

        if hero.return_flag_jump():
            number_of_jumps = 0

        if not list_mobs:
            running_level = False
            continue_level()

        all_sprites.update()
        all_sprites.draw(screen)

        hero_sprites.update()
        hero_sprites.draw(screen)

        attack_sprites.update()
        attack_sprites.draw(screen)

        attack_sprites_mobs.update()
        attack_sprites_mobs.draw(screen)

        mobs_sprites.update()
        mobs_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    running = True

    start_screen()

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 190) and \
                        (pygame.mouse.get_pos()[0] <= 700 and pygame.mouse.get_pos()[1] <= 270):
                    x1, y1 = event.pos
                    hero = Hero(load_image("hero_right.png"), 4, 1, list_textures, gravity,
                                list_rect_textures, list_mask_textures, list_mob_attack,
                                list_radiations, size, screen, view)
                    start_level()

                if (pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 490) and \
                        (pygame.mouse.get_pos()[0] <= 700 and pygame.mouse.get_pos()[1] <= 570):
                    pygame.quit()
