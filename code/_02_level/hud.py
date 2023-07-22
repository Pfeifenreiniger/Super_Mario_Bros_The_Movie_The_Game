
import pygame as pg
from code.fonts import FONT_PRESS_START_12

class HUD:
    def __init__(self, settings, player):
        self.settings = settings
        self.SCREEN = settings.get_display_screen()
        self.player = player
        self.font = FONT_PRESS_START_12
        self.life_image = pg.image.load("graphics/00_hud/life_player.png").convert_alpha()

    def display_lives(self):

        for x in range(self.player.lives):

            x_pos = x * (self.life_image.get_width() + 6)
            padding = pg.math.Vector2(15, 550)

            self.SCREEN.blit(self.life_image, (padding.x + x_pos, padding.y))

    def draw(self):

        self.display_lives()
