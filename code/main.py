
import pygame as pg

from settings import *
from events import EventLoop

from title_screen import TitleScreen


class Game:
    def __init__(self):
        # basic setup
        pg.init()
        self.event_loop = EventLoop()
        self.resolution = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.SCREEN = pg.display.set_mode(self.resolution)
        self.clock = pg.time.Clock()
        self.FPS = 30
        pg.display.set_caption("SUPER MARIO BROS. THE MOVIE: THE GAME")

        self.setup()

    def setup(self):
        self.title_screen = TitleScreen(event_loop=self.event_loop)

    def game_loop(self):

        while True:

            self.event_loop.loop_events()

            # delta time
            dt = self.clock.tick(self.FPS) / 1000


            self.title_screen.update(dt)



            # frame draw
            pg.display.set_caption(f"SUPER MARIO BROS. THE MOVIE: THE GAME | {round(self.clock.get_fps())} FPS")
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.game_loop()
