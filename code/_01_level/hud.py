
import pygame as pg
from code.fonts import FONT_PRESS_START_12

class HUD:
    def __init__(self, settings, player):
        self.settings = settings
        self.SCREEN = settings.get_display_screen()
        self.player = player
        self.font = FONT_PRESS_START_12
        self.life_image = pg.image.load("graphics/00_hud/life_player.png").convert_alpha()

    def display_health(self):

        def calc_hp(player) -> int:
            return round((player.health / player.max_health) * 100)

        text = f"HP: {calc_hp(self.player)}%"
        text_surf = self.font.render(text, False, (244, 244, 244))
        text_rect = text_surf.get_rect(topleft=(15, 565))

        self.SCREEN.blit(text_surf, text_rect)

    def display_lifes(self):

        for x in range(self.player.lives):

            x_pos = x * (self.life_image.get_width() + 6)
            padding = pg.math.Vector2(15, 520)

            self.SCREEN.blit(self.life_image, (padding.x + x_pos, padding.y))

    def draw(self):

        # display health
        self.display_health()

        # display lives
        self.display_lifes()
