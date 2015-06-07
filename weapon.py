import pygame
from settings import *


class Weapon(pygame.sprite.Sprite):

    def __init__(self, image_name, x=WINDOWWIDTH/2, y=WINDOWHEIGHT-5, power=1):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("images", image_name))
        self.rect_start = self.image.get_rect()
        self.is_active = False
        self.rect = self.rect_start.move(self.x - self.rect_start.centerx,
                                         self.y - self.rect_start.bottom)
        self.power = power

    def move_weapon_hero(self):
        if self.is_active:
            if self.rect.bottom <= 0:
                self.is_active = False
            else:
                self.rect = self.rect.move(0, -WEAPON_SPEED)
                self.y -= WEAPON_SPEED

    def move_weapon_enemy(self):
        if self.is_active:
            if self.rect.top >= WINDOWHEIGHT:
                self.is_active = False
            else:
                self.rect = self.rect.move(0, WEAPON_SPEED)
                self.y += WEAPON_SPEED
