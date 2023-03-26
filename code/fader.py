
import pygame as pg

class Fader:
    def __init__(self, settings):
        self.SCREEN = settings.get_display_screen()

        self.fade_rect = pg.Rect(0, 0, 800, 600)  # at position 0,0 with a width of 800 and a height of 600 pixels
        self.fade_surf = pg.Surface((800, 600))
        self.fade_surf.fill((0, 0, 0))

        self.alpha_value = 255

    def update(self):
        self.alpha_value -= 3

        if self.alpha_value <= 0:
            del self

    def draw(self):
        self.fade_surf.set_alpha(self.alpha_value)
        self.SCREEN.blit(self.fade_surf, self.fade_rect)
