from hero import *
from textures import *

hero = Hero
level = 'level_1'


def load_image(name, colorkey=None):
    fullname = os.path.join('levels/' + level + '/radiations', name)
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


class Radiation(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__(all_sprites)
        self.damage = 1

        self.image = load_image(image)
        self.rect = self.image.get_rect()

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        # self.dealing_damage()

    def dealing_damage(self, x, y):
        if -100 < self.rect.x - x < 100 and -100 < self.rect.y - y < 100:
            if self.rect.x - x == 0:
                return self.damage
            elif self.rect.x - x < 0:
                return self.damage * (1 / -(self.rect.x - x))
            return self.damage * (1 / (self.rect.x - x))
