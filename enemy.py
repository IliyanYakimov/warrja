import pygame
from settings import *
from weapon import Weapon
import random


class Enemy(pygame.sprite.Sprite):
    weapons = ["", 'enemywep1.png']
    healts = [0, 30, 50, 70]

    def __init__(self, image_name, level, health, x=WINDOWWIDTH/2, y=5):
        """level is an integer, for weapon's type"""
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("images", image_name))
        self.rect_start = self.image.get_rect()
        self.rect = self.rect_start.move(self.x - self.rect_start.right, 0)
        self.is_alive = True
        self.health = health
        self.move_left = False
        self.move_right = False
        self.level = level
        self.weapon = Weapon(Enemy.weapons[level], self.x, self.y)

    def move_and_shoot(self):
        if self.is_alive:
            if WINDOWWIDTH / 4 - ENEMY_SPEED / 2 <= self.x \
                    <= WINDOWWIDTH / 4 + ENEMY_SPEED / 2:
                if not random.randint(0, 1):
                    """if 0 go left, otherwise go right"""
                    self.move_left = True
                    self.move_right = False
                    self.weapon.move_weapon_enemy()
                else:
                    self.move_left = False
                    self.move_right = True
                    self.weapon.move_weapon_enemy()

            elif WINDOWWIDTH / 2 - ENEMY_SPEED / 2 <= self.x \
                    <= WINDOWWIDTH / 2 + ENEMY_SPEED / 2:
                if not random.randint(0, 1):
                    self.move_left = True
                    self.move_right = False
                    self.weapon.move_weapon_enemy()
                else:
                    self.move_left = False
                    self.move_right = True
                    self.weapon.move_weapon_enemy()

            elif 3 * WINDOWWIDTH / 4 - ENEMY_SPEED / 2 <= self.x \
                    <= 3 * WINDOWWIDTH / 4 + ENEMY_SPEED / 2:
                if not random.randint(0, 1):
                    self.move_left = True
                    self.move_right = False
                    self.weapon.move_weapon_enemy()
                else:
                    self.move_left = False
                    self.move_right = True
                    self.weapon.move_weapon_enemy()

            if self.move_left:
                self.x -= ENEMY_SPEED
                self.rect = self.rect.move(-ENEMY_SPEED, 0)
                self.weapon.move_weapon_enemy()
                if self.rect.left <= 5:
                    self.move_left = False
                    self.move_right = True
                    self.weapon.move_weapon_enemy()

            elif self.move_right:
                self.x += ENEMY_SPEED
                self.rect = self.rect.move(ENEMY_SPEED, 0)
                self.weapon.move_weapon_enemy()
                if self.rect.right >= WINDOWWIDTH - self.rect_start.right:
                    self.move_right = False
                    self.move_left = True
                    self.weapon.move_weapon_enemy()

            if not self.weapon.is_active:
                self.weapon.is_active = True
                self.weapon.rect.centerx = self.rect.centerx
                self.weapon.rect.centery = self.rect.centery
                self.weapon.x = self.x
                self.weapon.y = self.y
                self.weapon.move_weapon_enemy()
