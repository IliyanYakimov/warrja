from hero import *
from enemy import *
from bonus import *
import json
import sys


class Game:
    available_levels = [("1", None)]

    def __init__(self, level=1):
        self.hero = Hero()
        self.enemies = []
        self.playing_enemies = []
        self.bonuses = []
        self.current_bonus = None
        self.active_bonus = False
        self.final_bonus = False
        self.level = level
        self.is_running = True
        self.game_over = False
        self.is_completed = False
        self.restart = False
        self.level_completed = False
        with open('max_level_available', 'r') as \
                max_completed_level_file:
            max_level_available = max_completed_level_file.read()
            if max_level_available:
                self.max_level_available = int(max_level_available)

    def load_level(self, level):
        self.level = level
        self.hero.health = HERO_HEALTH
        self.playing_enemies = []
        self.restart = True
        self.hero.is_alive = True
        self.current_bonus = None
        self.active_bonus = False
        self.level_completed = False
        self.final_bonus = False
        print("tuka sme w load_level")
        self.hero.weapon = Weapon("weapon" + str(level) + ".png",
                                  self.hero.x, self.hero.y, level)

        if self.level > self.max_level_available:
            self.max_level_available = self.level
            with open('max_level_available', 'w') as \
                    max_completed_level_file:
                max_completed_level_file.write(str(self.max_level_available))
        
        with open('levels.json', 'r') as levels_file:
            levels = json.load(levels_file)
            current_level = levels[str(level)]
            for _ in range(current_level["enemies"]):
                self.enemies.append(
                        Enemy("enemy" + str(level) + ".png", level))
            self.bonuses = current_level['bonus_types']

    def enemy_collision(self):
        """check and action if you hit the enemy"""
        for enemy in self.playing_enemies:
            if pygame.sprite.collide_rect(self.hero.weapon, enemy):
                self.hero.weapon.is_active = False
                enemy.health -= self.hero.weapon.power
                if enemy.health <= 0:
                    enemy.is_alive = False
                    self.playing_enemies.remove(enemy)
                    if not self.active_bonus:
                        self.get_bonuses(enemy.x, enemy.y)
        
        if not self.enemies and not self.playing_enemies and\
                not self.final_bonus and not self.active_bonus:
            self.get_bonuses(WINDOWWIDTH / 2, 0)

        if self.active_bonus:
            self.current_bonus.get_bonus()


    def hero_collision(self):
        """check and action if enemy hit hero"""
        for enemy in self.playing_enemies:
            if pygame.sprite.collide_rect(enemy.weapon, self.hero) or \
                    pygame.sprite.collide_mask(self.hero, enemy.weapon):
                enemy.weapon.is_active = False
                self.hero.health -= enemy.weapon.power
                if self.hero.health <= 0:
                    self.hero.lives -= 1
                    if self.hero.lives <= 0:
                        self.game_over = True
                    else:
                        self.hero.is_alive = False
                return True
        return False

    def bonus_collision(self, bonus):
        if bonus:
            if pygame.sprite.collide_rect(bonus, self.hero):
                if bonus.bonus_type == 1:
                    if HERO_HEALTH - BONUS_RHEARTH <= \
                            self.hero.health <= HERO_HEALTH:
                        self.hero.health = HERO_HEALTH
                    else:
                        self.hero.health += BONUS_RHEARTH
                elif bonus.bonus_type == 2:
                    if self.hero.lives < 10:
                        self.hero.lives += 1
                elif bonus.bonus_type == 3:
                    self.hero.weapon.image = \
                            pygame.image.load(
                                    os.path.join("images", "weapon" + \
                                                 str(self.level + 1) + ".png"))
                    self.hero.weapon.power = self.level + 1
                    self.final_bonus = True
                    self.level_completed = True
                else:
                    self.is_completed = True
                del bonus
                self.active_bonus = False
                self.current_bonus = None
                return True
            return False


    def restart_level(self):
        self.load_level(self.level)


    def get_bonuses(self, x, y):
        if not self.enemies and not self.playing_enemies and \
                self.level < MAX_LEVEL:
            """this is for weapon bonus"""
            self.current_bonus = Bonus(x, y, "gift.png", 3)
            self.active_bonus = True
            return True
        if not self.enemies and not self.playing_enemies and \
                self.level == MAX_LEVEL:
            """this is for WINNER bonus"""
            self.current_bonus = Bonus(x, y, "winner.png", 4)
            self.active_bonus = True
            return True
        elif random.randint(1, 10) < 4:
            """30 percent chance for bonus"""
            rand = random.randint(1, 2)
            self.current_bonus = Bonus(x, y, Bonus.bonuses[rand], rand)
            self.active_bonus = True
            return True
        return False


    def loading_enemies(self):
        if self.level <= 3:
            if len(self.playing_enemies) < 4 and self.enemies:
                while len(self.playing_enemies) <= 4:
                    self.playing_enemies.append(self.enemies.pop())
        else:
            if len(self.playing_enemies) < 3 and self.enemies:
                while len(self.playing_enemies) <= 3:
                    self.playing_enemies.append(self.enemies.pop())


    def update(self):
        if self.level_completed and not self.is_completed:
            Game.available_levels.append((str(self.level + 1), None))
            self.load_level(self.level + 1)

        if self.game_over:
            self.is_running = False
            pygame.quit()
            sys.exit()

        if not self.hero.is_alive:
            self.restart_level()
        
        self.loading_enemies()
        for enemy in self.playing_enemies:
            enemy.move_and_shoot()

        self.hero_collision()
        self.hero.move()
        self.hero.shoot()
        self.enemy_collision()
        self.bonus_collision(self.current_bonus)
