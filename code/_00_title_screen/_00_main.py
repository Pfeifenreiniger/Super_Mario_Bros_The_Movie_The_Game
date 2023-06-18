
import pygame as pg
import sys

from code.menu_pane import MenuPane
from code.fonts import FONT_MASHEEN_BOLD_30, FONT_PRESS_START_20

class _00_Main:
    def __init__(self, event_loop, settings, locator):

        self.loaded = False

        self.settings = settings
        self.SCREEN = self.settings.get_display_screen()
        self.locator = locator

        # event loop - adding a custom event
        self.event_loop = event_loop
        CloudsTimerEvent(event_loop=self.event_loop)

        # inst objects
        self.sky = Sky(self.SCREEN)
        self.dinohattan = Dinohattan(self.SCREEN)
        self.koopahari_desert = KoopahariDesert(self.SCREEN)
        self.clouds = pg.sprite.Group()
        self.cloud_numb = 1
        Cloud(group=self.clouds, cloud_numb=self.cloud_numb)
        self.logo = Logo(self.SCREEN)
        self.logo_appearance = False
        self.press_start = PressStart(self.SCREEN)
        self.menu_pane = MenuPane(self.SCREEN, settings, self.locator)
        self.show_pane = False

        self.button_pressed = False
        self.button_pressed_timestamp = None

        # music
        self.music_volume = self.settings.music_volume
        self.music = pg.mixer.Sound("audio/music/Walk_the_Dinosaur_(GXSCC_Gameboy_Mix).mp3")
        self.music.set_volume(self.music_volume)
        self.music.play(loops=-1)

        # sfx
        self.sfx_volume = self.settings.sfx_volume
        self.press_start_sfx = pg.mixer.Sound("audio/sfx/menu/king_koopa_kill_that_plumber.mp3")
        self.press_start_sfx.set_volume(self.sfx_volume)

        # easter egg - Konami Code
        self.its_a_me_sfx = pg.mixer.Sound("audio/sfx/menu/sm64_mario_its__a_me.wav")
        self.its_a_me_sfx.set_volume(self.sfx_volume)
        self.correct_code = ["U", "U", "D", "D", "L", "R", "L", "R", "B", "A"]
        self.code_keys = []
        self.code_done = False

        # set inst_time attribute to logo object
        self.logo.inst_time = pg.time.get_ticks()

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True

    def check_setting_updates(self):
        if self.music_volume != self.settings.music_volume:
            self.music_volume = self.settings.music_volume
            self.music.set_volume(self.music_volume)

        if self.sfx_volume != self.settings.sfx_volume:
            self.sfx_volume = self.settings.sfx_volume
            self.its_a_me_sfx.set_volume(self.sfx_volume)
            self.press_start_sfx.set_volume(self.sfx_volume)

    def check_logo_appearance(self):
        if not self.logo_appearance and hasattr(self, "logo"):
            if pg.time.get_ticks() - self.logo.inst_time > 1500:
                self.logo_appearance = True

    def input(self):

        if not self.show_pane:

            if not self.button_pressed:

                def button_press_timestamp():
                    self.button_pressed = True
                    self.button_pressed_timestamp = pg.time.get_ticks()

                keys = pg.key.get_pressed()

                if keys[pg.K_SPACE] or keys[pg.K_RETURN]:

                    button_press_timestamp()

                    if not self.logo_appearance:
                        self.logo_appearance = True
                    if self.logo.xy_pos.y < 68:
                        self.logo.xy_pos.y = 68
                        self.logo.rect.y = round(self.logo.xy_pos.y)
                    else:
                        self.press_start_sfx.play()
                        self.show_pane = True
                        self.menu_pane.active = True
                        # to avoid accidentely pressing 'new game' on menu pane, menu pane will recognize that the player pressed a button
                        self.menu_pane.key_pressed = True
                        self.menu_pane.key_pressed_timestamp = pg.time.get_ticks()
                        self.logo_appearance = False
                        del self.logo

                if keys[pg.K_UP]:
                    button_press_timestamp()
                    self.code_keys.append('U')
                elif keys[pg.K_DOWN]:
                    button_press_timestamp()
                    self.code_keys.append('D')
                elif keys[pg.K_LEFT]:
                    button_press_timestamp()
                    self.code_keys.append('L')
                elif keys[pg.K_RIGHT]:
                    button_press_timestamp()
                    self.code_keys.append('R')
                elif keys[pg.K_a]:
                    button_press_timestamp()
                    self.code_keys.append('A')
                elif keys[pg.K_b]:
                    button_press_timestamp()
                    self.code_keys.append('B')
            else:
                if pg.time.get_ticks() - self.button_pressed_timestamp > 300:
                    self.button_pressed = False

    def check_konami_code(self):
        if not self.code_done:
            corr_keys = 0

            for key in self.code_keys:

                if corr_keys == 0:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 1:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 2:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 3:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 4:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 5:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 6:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 7:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 8:
                    if key == self.correct_code[corr_keys]:
                        corr_keys += 1
                elif corr_keys == 9:
                    if key == self.correct_code[corr_keys]:
                        self.code_done = True
                else:
                    corr_keys = 0

    def update(self, dt):

        # if event clouds timer event triggered
        if 'clouds_timer' in self.event_loop.triggered_events:
            self.cloud_numb = 1 if self.cloud_numb == 2 else 2
            Cloud(group=self.clouds, cloud_numb=self.cloud_numb)
            self.event_loop.triggered_events.remove('clouds_timer')

        self.input()

        self.check_konami_code()

        if self.code_done:
            self.its_a_me_sfx.play()
            self.code_done = False
            self.code_keys.clear()

        self.check_logo_appearance()

        self.dinohattan.update(dt)
        self.koopahari_desert.update(dt)

        for cloud in self.clouds:
            cloud.update(dt)

        if self.logo_appearance:
            self.logo.update(dt)

        if self.show_pane:
            self.menu_pane.update(dt)

        self.check_setting_updates()

        self.draw()

        if self.locator.current_location != 0:
            self.music.stop()

    def draw(self):
        self.sky.draw()

        for cloud in self.clouds:
            self.SCREEN.blit(cloud.image, cloud.rect)


        self.dinohattan.draw()
        self.koopahari_desert.draw()

        if self.logo_appearance:
            self.logo.draw()

        if self.logo_appearance and self.logo.xy_pos.y >= 68:
            self.press_start.draw()

        if self.show_pane:
            self.menu_pane.draw()


class KoopahariDesert:
    def __init__(self, screen):
        self.SCREEN = screen
        self.image = pg.image.load("graphics/00_title_screen/koopahari_desert.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=0, y=80)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed = 200

    def move(self, dt):
        if self.xy_pos.x <= -2350:
            self.xy_pos.x = 0
            self.rect.x = self.xy_pos.x
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)
        else:
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.SCREEN.blit(self.image, self.rect)

class Dinohattan:
    def __init__(self, screen):
        self.SCREEN = screen
        self.image_front = pg.image.load("graphics/00_title_screen/dinohattan_front.png").convert_alpha()
        self.xy_front = pg.math.Vector2(x=0, y=64)
        self.rect_front = self.image_front.get_rect(topleft = self.xy_front)
        self.image_back = pg.image.load("graphics/00_title_screen/dinohattan_back.png").convert_alpha()
        self.xy_back = pg.math.Vector2(x=0, y=251)
        self.rect_back = self.image_back.get_rect(topleft = self.xy_back)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed_front = 150
        self.speed_back = 100

    def move(self, dt):
        # front
        if self.xy_front.x <= -1428:
            self.xy_front.x = 0
            self.rect_front.x = self.xy_front.x
            self.xy_front.x += self.direction.x * self.speed_front * dt
            self.rect_front.x = round(self.xy_front.x)
        else:
            self.xy_front.x += self.direction.x * self.speed_front * dt
            self.rect_front.x = round(self.xy_front.x)

        # back
        if self.xy_back.x <= -1600:
            self.xy_back.x = 0
            self.rect_back.x = self.xy_back.x
            self.xy_back.x += self.direction.x * self.speed_back * dt
            self.rect_back.x = round(self.xy_back.x)
        else:
            self.xy_back.x += self.direction.x * self.speed_back * dt
            self.rect_back.x = round(self.xy_back.x)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.SCREEN.blit(self.image_back, self.rect_back)
        self.SCREEN.blit(self.image_front, self.rect_front)

class Sky:
    def __init__(self, screen):
        self.SCREEN = screen
        self.image = pg.image.load("graphics/00_title_screen/sky.png").convert()
        self.xy_pos = pg.math.Vector2(x=0, y=0)
        self.rect = self.image.get_rect(topleft=self.xy_pos)

    def draw(self):
        self.SCREEN.blit(self.image, self.rect)

class Cloud(pg.sprite.Sprite):
    def __init__(self, group, cloud_numb:int):
        super().__init__(group)
        self.image = pg.image.load(f"graphics/00_title_screen/clouds_{cloud_numb}.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=800, y=87) if cloud_numb == 1 else pg.math.Vector2(x=800, y=93)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed = 50

    def move(self, dt):
        if self.rect.right <= 0:
            self.kill()
        else:
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)

    def update(self, dt):
        self.move(dt)

class CloudsTimerEvent:
    def __init__(self, event_loop):
        self.event_loop = event_loop
        event_id = pg.USEREVENT + 1
        self.event_loop.EVENT_IDS['clouds_timer'] = event_id
        pg.time.set_timer(event_id, 12 * 1000)
        self.event_loop.add_event(event_id)

class Logo:
    def __init__(self, screen):
        self.SCREEN = screen
        self.image = pg.image.load("graphics/00_title_screen/logo.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=166, y=-193)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        # float based movement
        self.direction = pg.math.Vector2(x=0, y=1)
        self.speed = 100

    def move(self, dt):
        if self.xy_pos.y < 68:
            self.xy_pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.xy_pos.y)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.SCREEN.blit(self.image, self.rect)


class PressStart:
    def __init__(self, screen):
        self.SCREEN = screen
        font = FONT_MASHEEN_BOLD_30
        text = "PRESS START"
        self.text_surf =  font.render(text, False, (244, 244, 244))
        self.text_rect = self.text_surf.get_rect(center = (400, 510))

        self.blink_value = -1

    def slow_blink(self):
        self.blink_value += 0.06
        if self.blink_value > 1: self.blink_value = -1

        if self.blink_value >= 0: return True
        else: return False

    def draw(self):
        if self.slow_blink():
            self.SCREEN.blit(self.text_surf, self.text_rect)
