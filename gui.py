import pygame
from pygame.locals import *
from settings import *
from hero import *
from weapon import *
from enemy import *
from bonus import *
from game import *
from menu import *
import sys
from collections import OrderedDict


pygame.init()
pygame.display.set_caption('warrja')
displaysurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
fps_clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
font = pygame.font.SysFont('courier', 38)
game = Game()


image1 = pygame.image.load(os.path.join("images", "hero_right1.png"))
image2 = pygame.image.load(os.path.join("images", "hero_right2.png"))
image3 = pygame.image.load(os.path.join("images", "hero_right3.png"))
image4 = pygame.image.load(os.path.join("images", "hero_left1.png"))
image5 = pygame.image.load(os.path.join("images", "hero_left2.png"))
image6 = pygame.image.load(os.path.join("images", "hero_left3.png"))
hero_left_right = [image1, image2, image3, image4, image5, image6]


you_image = pygame.image.load(os.path.join("images", "you.png"))
enemies_image = pygame.image.load(os.path.join("images", "enemies.png"))


def start_level(level):
    game.is_running = True
    game.is_completed = False
    game.load_level(level)
    pygame.mouse.set_visible(False)
    main_menu.is_active = False
    while game.is_running:
        game.update()
        draw_level()
        handle_game_event()
        pygame.display.update()
        if game.is_completed or game.game_over or game.level_completed or \
                game.restart:
            pygame.time.delay(3000)
        
        if not game.hero.is_alive:
            pygame.time.delay(2500)
        
        if game.is_completed:
            main_menu.is_active = True
            start()
        if game.restart:
            game.restart = False
        fps_clock.tick(FPS)


BASICFONT = pygame.font.SysFont('courier', 18)


def show_start_screen():
    title_font = pygame.font.SysFont('courier', 100)
    title_surf1 = title_font.render('warrja', True, WHITE, BLUE)
    title_surf2 = title_font.render('warrja', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        displaysurf.fill(BLACK)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        displaysurf.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        displaysurf.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        fps_clock.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def draw_press_key_msg():
    press_key_surf = BASICFONT.render('Press a key to play.', True, RED)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOWWIDTH - 220, WINDOWHEIGHT - 30)
    displaysurf.blit(press_key_surf, press_key_rect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        quit()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        quit()
    return key_up_events[0].key


def start():
    show_start_screen()
    while main_menu.is_active:
        main_menu.draw_menu()
        handle_menu_event(main_menu)
        pygame.display.update()
        fps_clock.tick(FPS)


def quit():
    pygame.quit()
    sys.exit()


def back():
    level_menu.is_active = False


def menu_levels():
    level_menu.is_active = True
    while level_menu.is_active:
        level_menu.draw_menu()
        handle_menu_event(level_menu)
        pygame.display.update()
        fps_clock.tick(FPS)


Game.available_levels = [(str(level), start_level) for level in \
        range(1, game.max_level_available + 1)]
Game.available_levels.append(("BACK", back))
main_menu = Menu(OrderedDict([("NEW GAME", menu_levels),
                             ("QUIT", quit)]), displaysurf)
level_menu = Menu(OrderedDict(Game.available_levels), displaysurf)


def handle_menu_event(menu):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if menu == main_menu:
                    quit()
                else:
                    back()

            if event.key == K_DOWN and menu.current_option == None:
                menu.current_option = 0
                pygame.mouse.set_visible(False)

            elif event.key == K_UP and menu.current_option == None:
                menu.current_option = len(menu.options) - 1
                pygame.mouse.set_visible(False)

            elif event.key == K_DOWN and \
                    menu.current_option < len(menu.options) - 1:
                menu.current_option += 1

            elif event.key == K_DOWN and \
                    menu.current_option == len(menu.options) - 1:
                menu.current_option = 0

            elif event.key == K_UP and menu.current_option > 0:
                menu.current_option -= 1

            elif event.key == K_UP and menu.current_option == 0:
                menu.current_option = len(menu.options) - 1

            elif event.key == K_RETURN and menu.current_option is not None:
                if menu == main_menu:
                    menu.ready_options[menu.current_option].function()
                elif menu == level_menu and \
                        menu.ready_options[menu.current_option].text == "BACK":
                    menu.ready_options[menu.current_option].function()
                elif menu == level_menu:
                    level = menu.ready_options[menu.current_option]
                    start_level(int(level.text))


        elif event.type == MOUSEBUTTONUP:
            for option in menu.ready_options:
                if option.is_selected:
                    if menu == level_menu:
                        if option.text != 'BACK':
                            start_level(int(option.text))
                        else:
                            back()
                    else:
                        option.function()

        if pygame.mouse.get_rel() != (0, 0):
            menu.current_option = None


def handle_game_event():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.hero.move_left = True
            elif event.key == K_RIGHT:
                game.hero.move_right = True

            if event.key == K_SPACE:
                game.hero.weapon.is_active = True
                game.hero.shoot()

            if event.key == K_ESCAPE:
                quit()

        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.hero.move_left = False
            elif event.key == K_RIGHT:
                game.hero.move_right = False

        if event.type == pygame.QUIT:
            quit()


def draw_hero(hero):
    if hero.move_right:
        for i in range(3):
            displaysurf.blit(hero_left_right[i], hero.rect)
    elif hero.move_left:
        for i in range(3, 6):
            displaysurf.blit(hero_left_right[i], hero.rect)
    else:
        displaysurf.blit(hero.image, hero.rect)


def draw_enemy(enemy):
    displaysurf.blit(enemy.image, enemy.rect)


def draw_weapon(weapon):
    displaysurf.blit(weapon.image, weapon.rect)


def draw_enemy_weapon(weapon):
    displaysurf.blit(weapon.image, weapon.rect)


def draw_bonus(bonus):
    displaysurf.blit(bonus.image, bonus.rect)


def draw_game_msg(msg, color=VOLT):
    message = font.render(msg, True, color)
    rect = message.get_rect()
    rect.centerx = displaysurf.get_rect().centerx
    rect.centery = displaysurf.get_rect().centery
    displaysurf.blit(message, rect)


def draw_hero_lives():
    hero_image = pygame.transform.scale(game.hero.image, (20, 20))
    for live in range(game.hero.lives):
        displaysurf.blit(hero_image, (0,
                         WINDOWHEIGHT/2 - live*game.hero.rect.height/2))


def draw_hero_health():
    health_image = game.hero.health_image
    for h in range(1, game.hero.health + 1):
        displaysurf.blit(health_image, (WINDOWWIDTH - h*10, WINDOWHEIGHT - 15))
    displaysurf.blit(you_image,(WINDOWWIDTH - 50, WINDOWHEIGHT - 35))


def draw_enemy_health():
    health_image = game.hero.health_image
    """tricky"""
    for index, enemy in enumerate(game.playing_enemies):
        for h in range(1, enemy.health + 1):
            displaysurf.blit(health_image,
                             (WINDOWWIDTH - h*10, WINDOWHEIGHT/2 - index*11))
    displaysurf.blit(enemies_image,
                     (WINDOWWIDTH - 60, WINDOWHEIGHT/2 - (index+1)*11))


def draw_level():
    displaysurf.fill(WHITE)
    draw_hero(game.hero)
    draw_hero_health()
    draw_hero_lives()
    if game.hero.weapon.is_active:
        draw_weapon(game.hero.weapon)
    for enemy in game.playing_enemies:
        draw_enemy(enemy)
        draw_enemy_health()
        if enemy.weapon.is_active:
            draw_enemy_weapon(enemy.weapon)
    if game.current_bonus is not None:
        draw_bonus(game.current_bonus)
    if game.game_over:
        draw_game_msg("GAME OVER", RED)
    if game.is_completed:
        draw_game_msg("WIN ! You are the KING", BLUE)
    if game.level_completed and not game.is_completed:
        draw_game_msg('Level completed!', ROYAL_BLUE)
    if game.restart:
        draw_game_msg('Get ready!', VOLT)
