import pygame


class Hero:
    def __init__(self):
        self.coord = self.x, self.y = 525, 425
        self.damage = 25
        self.health = 100

    def movement(self):
        if self.x >= 0:
            if key:
                self.x += 1
            if key:
                self.x -= 1
            if key:
                self.y += 1