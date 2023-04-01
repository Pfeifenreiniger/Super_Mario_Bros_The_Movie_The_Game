
import pygame as pg

class Fader:
    def __init__(self, settings, fade_direct):
        self.SCREEN = settings.get_display_screen()
        self.fade_direct = fade_direct

        self.fade_rect = pg.Rect(0, 0, 800, 600)  # at position 0,0 with a width of 800 and a height of 600 pixels
        self.fade_surf = pg.Surface((800, 600))
        self.fade_surf.fill((0, 0, 0))

        self.set_alpha_value()

    def set_alpha_value(self):
        if self.fade_direct == "IN":
            self.alpha_value = 255
        else:
            self.alpha_value = 0

    def update(self):

        if self.fade_direct == "IN": # fade in
            self.alpha_value -= 3

        else: # fade out
            self.alpha_value += 3

    def draw(self):
        self.fade_surf.set_alpha(self.alpha_value)
        self.SCREEN.blit(self.fade_surf, self.fade_rect)
