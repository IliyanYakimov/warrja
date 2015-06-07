import unittest
from weapon import Weapon
from settings import *
import pygame


class TestWeapon(unittest.TestCase):

    def setUp(self):
        self.weapon = Weapon("weapon1.png")

    def test_position(self):
        self.assertEqual(self.weapon.x, WINDOWWIDTH/2)
        self.assertEqual(self.weapon.y, WINDOWHEIGHT-5)

    def test_weapon_has_image(self):
        self.assertIsNotNone(self.weapon.image,
                             'The hero doesn\'t have an image')

    def test_image_rect(self):
        self.assertIsInstance(self.weapon.rect, pygame.Rect)

    def test_weapon_is_active(self):
        self.assertFalse(self.weapon.is_active)

    def test_rect_image_positon(self):
        self.assertEqual(self.weapon.x, self.weapon.rect.centerx)

    def test_move_weapon_enemy(self):
        start_pos = self.weapon.y
        self.weapon.move_weapon_enemy()
        self.assertEqual(start_pos, self.weapon.y)
        self.weapon.is_active = True
        self.weapon.move_weapon_enemy()
        self.assertEqual(self.weapon.y, start_pos + WEAPON_SPEED)

    def test_move_weapon_hero(self):
        start_pos = self.weapon.y
        self.weapon.is_active = True
        self.weapon.move_weapon_hero()
        self.assertEqual(self.weapon.y, start_pos - WEAPON_SPEED)


if __name__ == '__main__':
    unittest.main()
