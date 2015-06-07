import unittest
from hero import Hero
from weapon import Weapon
from settings import *
import pygame


class TestHero(unittest.TestCase):

    def setUp(self):
        self.hero = Hero()

    def test_position(self):
        self.assertEqual(self.hero.x, WINDOWWIDTH / 2)
        self.assertEqual(self.hero.y, WINDOWHEIGHT - 5)

    def test_hero_has_image(self):
        self.assertIsNotNone(self.hero.image,
                             'The hero doesn\'t have an image')

    def test_image_rect(self):
        self.assertIsInstance(self.hero.rect, pygame.Rect)

    def test_is_alive(self):
        self.assertTrue(self.hero.is_alive)
        self.assertEqual(self.hero.health, 100)

    def test_hero_weapon(self):
        self.assertIsInstance(self.hero.weapon, Weapon)

    def test_move_attribute(self):
        self.assertFalse(self.hero.move_left)
        self.assertFalse(self.hero.move_right)

    def test_move(self):
        self.hero.move_right = True
        start_pos = self.hero.x
        self.hero.move()
        self.assertEqual(self.hero.x, start_pos + PLAYER_SPEED)
        self.assertEqual(self.hero.x, self.hero.rect.centerx)

    def test_weapon(self):
        self.assertFalse(self.hero.weapon.is_active)
        self.hero.shoot()
        self.assertTrue(self.hero.weapon.is_active)


if __name__ == '__main__':
    unittest.main()
