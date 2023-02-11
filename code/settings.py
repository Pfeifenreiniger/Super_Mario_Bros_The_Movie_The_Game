
import pygame as pg


class Settings:
    def __init__(self):

        # screen settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.resolution = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.screen_mode = "WINDOW"
        self.flags_window = pg.HWSURFACE|pg.DOUBLEBUF
        self.flags_fullscreen = pg.FULLSCREEN|pg.SCALED|pg.HWSURFACE|pg.DOUBLEBUF

        # audio settings
        self.music_volume = 1
        self.sfx_volume = 1

    def get_display_screen(self):
        if self.screen_mode == "WINDOW":
            return pg.display.set_mode(self.resolution, self.flags_window, 8)
        else:
            return pg.display.set_mode(self.resolution, self.flags_fullscreen, 8)

    def increase_volume(self, music_or_sfx:str):

        # music
        if music_or_sfx.startswith("mus"):
            if self.music_volume < 1:
                self.music_volume += 0.1
                self.music_volume = round(self.music_volume, 1)
        # sfx
        else:
            if self.sfx_volume < 1:
                self.sfx_volume += 0.1
                self.sfx_volume = round(self.sfx_volume, 1)

    def decrease_volume(self, music_or_sfx:str):

        # music
        if music_or_sfx.startswith("mus"):
            if self.music_volume > 0:
                self.music_volume -= 0.1
                self.music_volume = round(self.music_volume, 1)
        # sfx
        else:
            if self.sfx_volume > 0:
                self.sfx_volume -= 0.1
                self.sfx_volume = round(self.sfx_volume, 1)

