import pygame
from settings import *


class MenuOption(pygame.font.Font):

    def __init__(self, text, function, position=(0, 0),
                 font=None, font_color=WHITE, font_size=36):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.function = function
        self.position = position
        self.font_color = font_color
        self.font_size = font_size
        self.title = self.render(text, True, font_color)
        self.rect = self.title.get_rect(left=position[0],
                                        top=position[1])
        self.is_selected = False

    def set_position(self, x, y):
        self.position = x, y
        self.rect = self.title.get_rect(left=x, top=y)

    def highlight(self, color=GREEN):
        self.font_color = color
        self.title = self.render(self.text, True, self.font_color)
        self.is_selected = True

    def unhighlight(self):
        self.font_color = WHITE
        self.title = self.render(self.text, True, self.font_color)
        self.is_selected = False

    def check_for_mouse_selection(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.highlight()
        else:
            self.unhighlight()


class Menu:

    def __init__(self, options, display, bg_color=BLACK):
        """options is a dict for menu_options"""
        self.is_active = True
        self.options = options
        self.display = display
        self.bg_color = bg_color
        self.current_option = None
        self.ready_options = []
        for index, option in enumerate(options):
            menu_option = MenuOption(option, options[option])
            if menu_option.text == "BACK":
                menu_option.set_position(20 + menu_option.rect.width/2,
                                         20 + menu_option.rect.height/2)
            else:
                option_pos_x = WINDOWWIDTH/2 - menu_option.rect.width/2
                option_pos_y = WINDOWHEIGHT/2 + index*menu_option.rect.height
                menu_option.set_position(option_pos_x, option_pos_y)
            self.ready_options.append(menu_option)

    def draw_menu(self):
        self.display.fill(self.bg_color)
        for option in self.ready_options:
            option.check_for_mouse_selection()
            if self.current_option is not None:
                self.ready_options[self.current_option].highlight()
            self.display.blit(option.title, option.position)
