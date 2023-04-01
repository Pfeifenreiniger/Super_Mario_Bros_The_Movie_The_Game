
import pygame as pg

from code.fader import Fader

class _00_Logos:
    def __init__(self, settings):

        self.loaded = False

        self.settings = settings
        SCREEN = self.settings.get_display_screen()

        self.fader_out = Fader(settings, "OUT")
        self.fader_in = Fader(settings, "IN")

        self.nonetendo_logo = NonetendoLogo(SCREEN, settings)
        self.nonetendo_timestamp = None
        self.nonetendo_show = False

        self.pfeife_logo = PfeifeTelespiele(SCREEN)
        self.pfeife_timestamp = None
        self.pfeife_show = False

        self.logos_done = False

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True
            self.nonetendo_show = True
            self.nonetendo_timestamp = pg.time.get_ticks()
            self.pfeife_timestamp = pg.time.get_ticks()

    def update(self, dt):

        if self.nonetendo_show:
            if pg.time.get_ticks() - self.nonetendo_timestamp < 4500:
                self.nonetendo_logo.update(dt)
                self.nonetendo_logo.draw()
            else:
                if self.fader_out.alpha_value >= 255:
                    self.nonetendo_show = False
                    self.pfeife_timestamp = pg.time.get_ticks()
                    self.pfeife_show = True
                    self.fader_out.set_alpha_value()
                else:
                    self.fader_out.update()
                    self.fader_out.draw()
        elif self.pfeife_show:
            self.pfeife_logo.draw()
            if pg.time.get_ticks() - self.pfeife_timestamp < 3500:
                if self.fader_in.alpha_value > 0:
                    self.fader_in.update()
                    self.fader_in.draw()
            else:
                if self.fader_out.alpha_value >= 255:
                    self.pfeife_show = False
                    self.logos_done = True
                else:
                    self.fader_out.update()
                    self.fader_out.draw()


class NonetendoLogo:
    def __init__(self, screen, settings):
        self.SCREEN = screen

        self.image_nonetendo = pg.image.load("graphics/00_startup_logos/nonetendo/nonetendo.png").convert_alpha()
        self.xy_nonetendo = pg.math.Vector2(x=400, y=-26)
        self.y_stop_nonetendo = 275
        self.rect_nonetendo = self.image_nonetendo.get_rect(center=self.xy_nonetendo)

        self.image_presents = pg.image.load("graphics/00_startup_logos/nonetendo/presents.png").convert_alpha()
        self.xy_presents = pg.math.Vector2(x=400, y=325)
        self.rect_presents = self.image_presents.get_rect(center=self.xy_presents)

        # float based movement
        self.direction = pg.math.Vector2(x=0, y=1)
        self.speed_nonetendo = 150
        self.move_done = False

        # sfx
        sfx_volume = settings.sfx_volume
        self.toilet_sfx = pg.mixer.Sound("audio/sfx/startup_logos/toilet-flushing.mp3")
        self.toilet_sfx.set_volume(sfx_volume)

    def move(self, dt):
        if self.xy_nonetendo.y < self.y_stop_nonetendo:
            self.xy_nonetendo.y += self.direction.y * self.speed_nonetendo * dt
            self.rect_nonetendo.y = round(self.xy_nonetendo.y)
        else:
            self.xy_nonetendo.y = self.y_stop_nonetendo
            self.rect_nonetendo.y = round(self.xy_nonetendo.y)
            self.toilet_sfx.play()
            self.move_done = True

    def update(self, dt):
        if not self.move_done:
            self.move(dt)

    def draw(self):
        self.SCREEN.fill((0, 0, 0)) # black bg
        self.SCREEN.blit(self.image_nonetendo, self.rect_nonetendo)

        if self.move_done:
            self.SCREEN.blit(self.image_presents, self.rect_presents)

class PfeifeTelespiele:
    def __init__(self, screen):
        self.SCREEN = screen

        self.image = pg.image.load("graphics/00_startup_logos/pfeife_telespiele/pfeife_telespiele.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=400, y=300)
        self.rect = self.image.get_rect(center=self.xy_pos)

    def draw(self):
        self.SCREEN.fill((0, 0, 0))  # black bg
        self.SCREEN.blit(self.image, self.rect)
