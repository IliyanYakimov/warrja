from hero import *
from enemy import *
from bonus import *


class Game:

    def __init__(self, level=1):
        self.hero = Hero()
        self.enemies = []
        self.bonuses = []
        self.level = level
        self.is_running = True
        self.game_over = False
