import pygame
from settings import *


class Bonus(pygame.sprite.Sprite):
    bonuses = ["", "rheart.png", "bheart.png", "bonus_wep"]

    def __init__(self, x, y, image_name, bonus_type):
        """bonus_type is an integer. Meaning: index for bonuses list"""
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("images", image_name))
        self.rect = self.image.get_rect()
        self.bonus_type = bonus_type

    def get_bonus(self):
        if self.rect.bottom <= WINDOWHEIGHT:
            self.y += BONUS_SPEED
            self.rect = self.rect.move(0, BONUS_SPEED)
