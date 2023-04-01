
import pygame as pg

from code.fader import Fader
from code.fonts import FONT_MASHEEN_BOLD_40
from code.fonts import FONT_PRESS_START_14

class GameOverScreen:
    def __init__(self, settings):
        self.SCREEN = settings.get_display_screen()

        self.music = pg.mixer.Sound("audio/music/FainGames - Cyberpunk 8-bit Relaxing Music.mp3")
        self.music_play = False

        self.restart_level = False
        self.restart_game = False

        self.fader = Fader(settings, "IN")

        self.main_font = FONT_MASHEEN_BOLD_40
        self.second_font = FONT_PRESS_START_14

        # main
        self.main_text = "KING KOOPA WINS"
        self.main_text_surf = self.main_font.render(self.main_text, False, (244, 244, 244))
        self.main_text_rect = self.main_text_surf.get_rect(center=(400, 300))

        # second
        self.blink_value = -1

        self.second_text1 = "Press Enter to restart the level,"
        self.second_text2 = "Escape to go back to the main menu"

        self.second_text1_surf = self.second_font.render(self.second_text1, False, (244, 244, 244))
        self.second_text1_rect = self.second_text1_surf.get_rect(center=(400, 415))

        self.second_text2_surf = self.second_font.render(self.second_text2, False, (244, 244, 244))
        self.second_text2_rect = self.second_text2_surf.get_rect(center=(400, 434))

        # key inputs
        self.key_pressed = True
        self.key_pressed_timestamp = pg.time.get_ticks()

    def display_main(self):
        """black screen bg and main game over text"""
        self.SCREEN.fill((36, 36, 36))

        self.SCREEN.blit(self.main_text_surf, self.main_text_rect)

    def display_second(self):
        """text of key inputs"""

        if self.slow_blink():
            self.SCREEN.blit(self.second_text1_surf, self.second_text1_rect)
            self.SCREEN.blit(self.second_text2_surf, self.second_text2_rect)

    def slow_blink(self):
        self.blink_value += 0.04
        if self.blink_value > 1: self.blink_value = -1

        if self.blink_value >= 0: return True
        else: return False

    def fade_in(self):

        if self.fader.alpha_value > 0:
            self.fader.update()
            self.fader.draw()

    def input(self):

        if not self.key_pressed:

            keys = pg.key.get_pressed()

            if keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]:
                self.restart_level = True
            elif keys[pg.K_ESCAPE]:
                self.restart_game = True
        else:
            if pg.time.get_ticks() - self.key_pressed_timestamp >= 400:
                self.key_pressed = False

    def update(self):

        if not self.music_play:
            self.music.play(loops=-1)
            self.music_play = True

        self.input()

    def draw(self):

        # main screen components (black bg and game over text)
        self.display_main()

        # secondary screen components (blinking text of which keys to press)
        self.display_second()

        # fade in
        self.fade_in()

        self.input()
