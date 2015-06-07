import pygame
from settings import *
from weapon import Weapon


class Hero(pygame.sprite.Sprite):

    def __init__(self, x=WINDOWWIDTH/2, y=WINDOWHEIGHT-5):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("images", "hero1.png"))
        self.rect_start = self.image.get_rect()
        self.rect = self.rect_start.move(
            self.x-self.rect_start.centerx, self.y)
        self.is_alive = True
        self.health = 100
        self.lives = STARTING_LIVES
        self.weapon = Weapon("weapon1.png", x, y)
        self.move_left = False
        self.move_right = False

    def move(self):
        if self.move_right and \
                self.rect.right <= WINDOWWIDTH-self.rect_start.centerx:
            self.x += PLAYER_SPEED
            self.rect = self.rect.move(PLAYER_SPEED, 0)
        elif self.move_left and self.rect.left >= self.rect_start.centerx:
            self.x -= PLAYER_SPEED
            self.rect = self.rect.move(-PLAYER_SPEED, 0)

    def shoot(self):
        self.weapon.is_active = True
        self.weapon.move_weapon_hero()
