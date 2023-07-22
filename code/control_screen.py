
import pygame as pg

from code.fonts import FONT_PRESS_START_12
from code.fader import Fader

class ControlScreen:
    def __init__(self, level:int, settings):
        self.loaded = False

        self.lvl = level
        self.font = FONT_PRESS_START_12
        self.load_keys()
        self.load_bg()

        self.SCREEN = settings.get_display_screen()

        self.fader_out = Fader(settings, "OUT")
        self.fader_in = Fader(settings, "IN")

        self.ready = False
        self.end = False
        self.done = False

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True

    def load_keys(self):

        root_folder = 'graphics/00_control_keys/'

        # images all keys
        keys_all = ["up", "down", "left", "right", "space", "return", "escape"]
        self.key_images = {key: pg.image.load(f'{root_folder}{key}.png').convert_alpha() for key in keys_all}

        # rects and texts
        y_img = 300
        y_txt = y_img + 80
        xs = []
        keys = []
        if self.lvl == 1:
            xs = [i * round(800 / 7) for i in range(7) if i != 0]  # bei 6 geplanten Bildern 7, da man auch padding zum rechten Rand braucht
            rgb = (244, 244, 244)
            key_texts = ["left", "right", "jump", "duck", "attack", "menu"]
            keys_in_use = ["left", "right", "up", "down", "space", "escape"]

        elif self.lvl == 2:
            xs = [i * round(800 / 6) for i in range(6) if i != 0]
            rgb = (244, 244, 244)
            key_texts = ["left", "right", "up", "down", "menu"]
            keys_in_use = ["left", "right", "up", "down", "escape"]

        self.keys_in_use = keys_in_use.copy()

        # rects
        self.key_rects = {key : self.key_images[key].get_rect(center=(xs[i], y_img)) for i, key in enumerate(keys_in_use)}

        # texts
        self.key_texts = {}
        for i, key in enumerate(keys_in_use):
            key_text_surf = self.font.render(key_texts[i], False, rgb)
            key_text_rect = key_text_surf.get_rect(center=(xs[i], y_txt))
            self.key_texts[key] = (key_text_surf, key_text_rect)


    def load_bg(self):
        if self.lvl == 1:
            self.bg_image = pg.image.load('graphics/01_excavation_site/controls/01_controls_screen.png').convert()
        elif self.lvl == 2:
            self.bg_image = pg.image.load('graphics/02_streets_of_dinohattan/controls/02_controls_screen.png').convert()

        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def fade_in(self):
        if self.fader_in.alpha_value > 0:
            self.fader_in.update()
            self.fader_in.draw()
        else:
            self.ready = True

    def fade_out(self):
        if self.fader_out.alpha_value < 255:
            self.fader_out.update()
            self.fader_out.draw()
        else:
            self.done = True

    def input(self):

        if not self.end:
            keys = pg.key.get_pressed()

            if keys[pg.K_SPACE] or keys[pg.K_RETURN] or keys[pg.K_ESCAPE] or keys[pg.K_KP_ENTER]:
                self.end = True

    def draw(self):

        # background image
        self.SCREEN.blit(self.bg_image, self.bg_rect)

        # key controls
        for key in self.keys_in_use:
            # key image
            self.SCREEN.blit(self.key_images[key], self.key_rects[key])
            # key text
            self.SCREEN.blit(self.key_texts[key][0], self.key_texts[key][1])

        # fade out if end
        if self.end:
            self.fade_out()

    def update(self):

        if self.ready:
            self.draw()
            self.input()
        else:
            self.fade_in()
