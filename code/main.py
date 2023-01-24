
import pygame as pg
pg.init()

from settings import Settings
from events import EventLoop

from _00_title_screen.title_screen import TitleScreen
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

        self.setup()

    def setup(self):
        # self.title_screen = TitleScreen(event_loop=self.event_loop, settings=self.settings)
        self._01_level = _01_Main(event_loop=self.event_loop, settings=self.settings)

    def game_loop(self):

        while 1:

            self.event_loop.loop_events()

            # delta time
            dt = self.clock.tick(self.FPS) / 1000

            self.SCREEN.fill('black')
            # self.title_screen.update(dt)
            self._01_level.update(dt)



            # frame draw
            pg.display.set_caption(f"SUPER MARIO BROS. THE MOVIE: THE GAME | {round(self.clock.get_fps())} FPS")
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.game_loop()
