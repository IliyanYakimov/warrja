import unittest
from bonus import Bonus
from settings import *
import pygame


class TestBonus(unittest.TestCase):

    def setUp(self):
        self.bonus = Bonus(WINDOWWIDTH/2, 5, "rheart.png", 1)

    def test_position(self):
        self.assertEqual(self.bonus.x, WINDOWWIDTH/2)
        self.assertEqual(self.bonus.y, 5)

    def test_bonus_has_image(self):
        self.assertIsNotNone(self.bonus.image,
                             'The hero doesn\'t have an image')

    def test_bonus_rect(self):
        self.assertIsInstance(self.bonus.rect, pygame.Rect)

    def test_bonus_type(self):
        self.assertEqual(self.bonus.bonus_type, 1)

    def test_get_bonus(self):
        start_pos = self.bonus.x
        self.bonus.get_bonus()
        self.assertEqual(self.bonus.y, 5 + BONUS_SPEED)


if __name__ == '__main__':
    unittest.main()
