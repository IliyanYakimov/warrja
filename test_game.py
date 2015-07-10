import unittest
from game import *


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_load_level(self):
        self.assertFalse(self.game.restart)
        self.assertFalse(self.game.bonuses)
        self.assertIsNone(self.game.current_bonus)
        self.assertFalse(self.game.game_over)
        self.game.load_level(1)
        self.assertEqual(self.game.level, 1)
        self.assertTrue(self.game.restart)
        with open('levels.json', 'r') as levels_file:
            levels = json.load(levels_file)
            level = levels[str(self.game.level)]
        self.assertEqual(len(self.game.enemies), level['enemies'])
        self.assertEqual(self.game.bonuses, level['bonus_types'])

    def test_enemy_collision(self):
        enemy1 = Enemy("enemywep1.png", 1)
        enemy2 = Enemy("enemywep1.png", 1)
        self.game.playing_enemies.append(enemy1)
        self.game.playing_enemies.append(enemy2)
        self.game.hero.weapon.is_active = True
        self.game.enemy_collision()
        self.assertTrue(self.game.hero.weapon.is_active)
        self.assertTrue(enemy1.is_alive)
        self.assertTrue(enemy2.is_alive)
        self.assertEqual(enemy1.health, Enemy.healths[1])
        self.assertEqual(enemy2.health, Enemy.healths[1])
        enemy1.rect.centerx = self.game.hero.weapon.rect.centerx
        enemy1.rect.centery = self.game.hero.weapon.rect.centery
        enemy1.x = self.game.hero.weapon.x
        enemy1.y = self.game.hero.weapon.y
        self.game.enemy_collision()
        self.assertFalse(self.game.hero.weapon.is_active)
        self.assertEqual(enemy1.health,
                         Enemy.healths[1] - self.game.hero.weapon.power)
        self.assertTrue(enemy1.is_alive)
        self.assertEqual(enemy2.health, Enemy.healths[1])
        while enemy1.is_alive:
            self.game.enemy_collision()
        self.assertFalse(enemy1.is_alive)
        self.assertIsNot(enemy1, self.game.playing_enemies[0])


    def test_hero_collision(self):
        enemy1 = Enemy("enemywep1.png", 1)
        enemy1.weapon.is_active = True
        self.game.playing_enemies.append(enemy1)
        self.assertTrue(enemy1.weapon.is_active)
        self.assertFalse(self.game.hero_collision())
        self.assertEqual(self.game.hero.health, HERO_HEALTH)
        enemy1.weapon.rect.centerx = self.game.hero.rect.centerx
        enemy1.weapon.rect.centery = self.game.hero.rect.centery
        self.assertTrue(self.game.hero_collision())
        self.assertFalse(enemy1.weapon.is_active)
        self.assertEqual(self.game.hero.health,
                         HERO_HEALTH - enemy1.weapon.power)
        while self.game.hero.health > 0:
            self.game.hero_collision()
        self.assertEqual(self.game.hero.lives, STARTING_LIVES - 1)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.hero.is_alive)
        while self.game.hero.lives > 0:
            self.game.hero_collision()
        self.assertFalse(self.game.hero.is_alive)
        self.assertTrue(self.game.game_over)


    def test_bonus_collision(self):
        bonus1 = Bonus(WINDOWWIDTH/2, 0, "rheart.png", 1)
        self.assertFalse(self.game.bonus_collision(bonus1))
        bonus1.rect.centerx = self.game.hero.rect.centerx
        bonus1.rect.centery = self.game.hero.rect.centery
        self.game.hero.health = HERO_HEALTH - BONUS_RHEARTH
        self.assertTrue(self.game.bonus_collision(bonus1))
        self.assertEqual(HERO_HEALTH, self.game.hero.health)
        self.game.hero.health = 1
        self.assertTrue(self.game.bonus_collision(bonus1))
        self.assertEqual(self.game.hero.health, 1 + BONUS_RHEARTH)
        del bonus1
        bonus2 = Bonus(WINDOWWIDTH/2, 0, "bheart.png", 2)
        self.assertFalse(self.game.bonus_collision(bonus2))
        bonus2.rect.centerx = self.game.hero.rect.centerx
        bonus2.rect.centery = self.game.hero.rect.centery
        self.assertTrue(self.game.bonus_collision(bonus2))
        self.assertEqual(self.game.hero.lives, STARTING_LIVES + 1)
        self.game.hero.lives = 10
        self.assertTrue(self.game.bonus_collision(bonus2))
        self.assertEqual(self.game.hero.lives, 10)
        del bonus2
        bonus3 = Bonus(WINDOWWIDTH/2, 0, "gift.png", 3)
        self.assertFalse(self.game.bonus_collision(bonus3))
        bonus3.rect.centerx = self.game.hero.rect.centerx
        bonus3.rect.centery = self.game.hero.rect.centery
        self.assertFalse(self.game.final_bonus)
        self.assertFalse(self.game.level_completed)
        self.assertTrue(self.game.bonus_collision(bonus3))
        self.assertTrue(self.game.final_bonus)
        self.assertTrue(self.game.level_completed)
        self.assertEqual(self.game.hero.weapon.power, self.game.level + 1)
        self.assertIsNone(self.game.current_bonus)
        self.assertFalse(self.game.active_bonus)

    def test_get_bonuses(self):
        self.assertTrue(self.game.get_bonuses(WINDOWWIDTH/2, 0))
        self.assertLess(self.game.current_bonus.bonus_type, 4)
        self.game.level = MAX_LEVEL
        self.game.get_bonuses(WINDOWWIDTH/2, 0)
        self.assertEqual(self.game.current_bonus.bonus_type, 4)


if __name__ == '__main__':
    unittest.main()
