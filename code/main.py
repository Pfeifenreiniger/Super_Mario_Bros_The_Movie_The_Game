
import pygame as pg
pg.init()

from settings import Settings
from events import EventLoop
from locator import Locator

from _00_title_screen._00_main import _00_Main
from _01_level._01_main import _01_Main


class Game:
    def __init__(self):
        # basic setup
        self.event_loop = EventLoop()
        self.settings = Settings()
        self.SCREEN = self.settings.get_display_screen()
        self.clock = pg.time.Clock()
        self.FPS = 30
        pg.display.set_caption("SUPER MARIO BROS. THE MOVIE: THE GAME")

        self.locator = Locator()
        self.old_current_location = self.locator.current_location

        self.setup()

    def setup(self):
        if self.locator.current_location == 0:
            self.title_screen = _00_Main(event_loop=self.event_loop, settings=self.settings, locator=self.locator)
        elif self.locator.current_location == 1:
            self._01_level = _01_Main(event_loop=self.event_loop, settings=self.settings, locator=self.locator)

    def game_loop(self):

        while 1:

            self.event_loop.loop_events()

            # delta time
            dt = self.clock.tick(self.FPS) / 1000

            if self.old_current_location != self.locator.current_location:
                self.old_current_location = self.locator.current_location
                self.setup()

            if self.locator.current_location == 0:
                self.title_screen.update(dt)
            elif self.locator.current_location == 1:
                self._01_level.update(dt)



            # frame draw
            pg.display.set_caption(f"SUPER MARIO BROS. THE MOVIE: THE GAME | {round(self.clock.get_fps())} FPS")
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.game_loop()
