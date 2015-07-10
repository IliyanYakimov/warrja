import unittest
import pygame
from enemy import Enemy
from weapon import Weapon
from settings import *


class TestEnemy(unittest.TestCase):

    def setUp(self):
        self.enemy = Enemy("enemy1.png", 1)

    def test_position(self):
        self.assertEqual(self.enemy.x, WINDOWWIDTH/2)
        self.assertEqual(self.enemy.y, 5)

    def test_enemy_has_image(self):
        self.assertIsNotNone(self.enemy.image,
                             'The hero doesn\'t have an image')

    def test_image_rect(self):
        self.assertIsInstance(self.enemy.rect, pygame.Rect)

    def test_is_alive(self):
        self.assertTrue(self.enemy.is_alive)
        self.assertEqual(self.enemy.health, 5)

    def test_move_attribute(self):
        self.assertFalse(self.enemy.move_left)
        self.assertFalse(self.enemy.move_right)

    def test_level(self):
        self.assertEqual(self.enemy.level, 1)

    def test_hero_weapon(self):
        self.assertIsInstance(self.enemy.weapon, Weapon)


if __name__ == '__main__':
    unittest.main()
