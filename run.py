import pygame
from settings import *
from hero import *
from weapon import *
from pygame.locals import *
from enemy import *
from bonus import *
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
enemy = Enemy("enemy1.png", 1, 30)
enemy.move_right = True
enemy.weapon.is_active = True

bonus = Bonus(enemy.x, enemy.y, "rheart.png", 1)

while True:
    DISPLAYSURF.fill(WHITE)
    hero.move()
    hero.shoot()
    enemy.move_and_shoot()
    bonus.get_bonus()


    DISPLAYSURF.blit(hero.weapon.image, (320, hero.weapon.rect.top))
    DISPLAYSURF.blit(hero.image, (hero.x, 440))
    DISPLAYSURF.blit(enemy.image, (enemy.x, 20))
    DISPLAYSURF.blit(enemy.weapon.image, (enemy.weapon.x, enemy.weapon.rect.bottom))
    DISPLAYSURF.blit(bonus.image, (bonus.x, bonus.rect.top))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps_clock.tick(FPS)