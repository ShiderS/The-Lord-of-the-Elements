from hero import *

hero = Hero


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


radiation_sprites = pygame.sprite.Group()


class Radiation(pygame.sprite.Sprite):
    image = load_image("radiation.png")

    def __init__(self):
        super().__init__(radiation_sprites)
        self.damage = 2

        self.image = Radiation.image
        self.rect = self.image.get_rect()

        self.rect.x = 175
        self.rect.y = 185

        # self.dealing_damage()

    def dealing_damage(self, x, y):
        if -100 < self.rect.x - x < 100 and -100 < self.rect.y - y < 100:
            return self.damage
