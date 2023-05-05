
import pygame as pg
pg.init()


from code.settings import Settings
from code.event_loop import EventLoop
from code.locator import Locator

from code._00_startup_logos._00_logos import _00_Logos
from code._00_title_screen._00_main import _00_Main
from code._01_level._01_main import _01_Main


class GameLoop:
    def __init__(self):
        # basic setup
        self.settings = Settings()
        self.event_loop = EventLoop(self.settings)
        self.clock = pg.time.Clock()
        self.FPS = 30
        pg.display.set_caption("SUPER MARIO BROS. THE MOVIE: THE GAME")
        self.first_start = True

        self.locator = Locator()
        self.old_current_location = self.locator.current_location

        self.setup()

    def setup(self):
        """loads the current level or main title screen"""

        self.garbage_cleanup()

        if self.locator.current_location == 0:
            if self.first_start:
                self._00_startup_logos = _00_Logos(settings=self.settings)
            else:
                self._00_screen = _00_Main(event_loop=self.event_loop, settings=self.settings, locator=self.locator)
        elif self.locator.current_location == 1:
            self._01_level = _01_Main(event_loop=self.event_loop, settings=self.settings, locator=self.locator)

    def garbage_cleanup(self):
        """get rid of currently not used levels"""

        if self.locator.current_location == 0:
            if hasattr(self, '_01_level'):
                del self._01_level
        elif self.locator.current_location == 1:
            if hasattr(self, '_00_startup_logos'):
                del self._00_startup_logos
            if hasattr(self, '_00_screen'):
                self._00_screen.press_start_sfx.stop()
                del self._00_screen

    def looping(self):

        while 1:

            self.event_loop.loop_events()

            # delta time
            dt = self.clock.tick(self.FPS) / 1000

            if not self.first_start:
                if self.old_current_location != self.locator.current_location:
                    self.old_current_location = self.locator.current_location
                    self.setup()

            if self.locator.current_location == 0:
                if self.first_start:
                    if self._00_startup_logos.loaded:
                        self._00_startup_logos.update(dt)
                        if self._00_startup_logos.logos_done:
                            self.first_start = False
                            self.setup()
                    else:
                        self._00_startup_logos.check_loading_progression()
                else:
                    if self._00_screen.loaded:
                        self._00_screen.update(dt)
                    else:
                        self._00_screen.check_loading_progression()
            elif self.locator.current_location == 1:
                if self._01_level.loaded:
                    if not self._01_level.intro.done:
                        self._01_level.intro.update(dt)
                    else:
                        self._01_level.update(dt)
                else:
                    self._01_level.check_loading_progression()



            # frame draw
            pg.display.set_caption(f"SUPER MARIO BROS. THE MOVIE: THE GAME | {round(self.clock.get_fps())} FPS")
            pg.display.update()
