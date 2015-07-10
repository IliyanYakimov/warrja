import pygame
from settings import *
from hero import *
from weapon import *
from pygame.locals import *
from enemy import *
from bonus import *
from game import *
import sys


pygame.init()
DISPLAYSURF = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('TEST')
fps_clock = pygame.time.Clock()

hero = Hero()
hero.move_right = True

wep = Weapon("weapon1.png")
wep.is_active = True
print(wep.rect.right)
print(wep.x)
print(wep.rect.centerx)
enemy = Enemy("enemy1.png", 1)
enemy.move_right = True
enemy.weapon.is_active = True

bonus = Bonus(enemy.x, enemy.y, "rheart.png", 1)

game = Game(1)
game.load_level(1)
game.hero.move_right = True



while True:
    DISPLAYSURF.fill(WHITE)
    #hero.move()
    #hero.shoot()
    #enemy.move_and_shoot()
    game.hero.move()
    game.hero.shoot()
    bonus.get_bonus()
    for j in range(4):
        game.enemies[j].is_active = True
        game.enemies[j].move_and_shoot()

    if game.hero.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        print("yeah")
    
    print(pygame.mouse.get_rel())
    #DISPLAYSURF.blit(hero.weapon.image, (320, hero.weapon.rect.top))
    #DISPLAYSURF.blit(hero.image, (hero.x, 440))
    #DISPLAYSURF.blit(enemy.image, (enemy.x, 20))
    #DISPLAYSURF.blit(enemy.weapon.image, (enemy.weapon.x, enemy.weapon.rect.bottom))
    DISPLAYSURF.blit(game.hero.image, (game.hero.x, 440))
    DISPLAYSURF.blit(game.hero.weapon.image, (320, game.hero.weapon.rect.top))
    for i in range(4):
        DISPLAYSURF.blit(game.enemies[i].image, (game.enemies[i].x, 20))
        DISPLAYSURF.blit(game.enemies[i].weapon.image, (game.enemies[i].weapon.x, game.enemies[i].weapon.rect.bottom))
    DISPLAYSURF.blit(bonus.image, (bonus.x, bonus.rect.top))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps_clock.tick(FPS)