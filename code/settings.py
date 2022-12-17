

class Settings:
    def __init__(self):

        # screen settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.screen_mode = "WINDOW"

        # audio settings
        self.music_volume = 1
        self.sfx_volume = 1

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

