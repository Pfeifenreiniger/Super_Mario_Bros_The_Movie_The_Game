
import pygame as pg
import sys

from fonts import FONT_MASHEEN_BOLD_30, FONT_PRESS_START_20


class TitleScreen:
    def __init__(self, event_loop, settings):
        self.SCREEN = pg.display.get_surface()
        self.settings = settings

        # event loop - adding a custom event
        self.event_loop = event_loop
        clouds_timer = pg.event.custom_type()
        pg.time.set_timer(clouds_timer, 12 * 1000)
        self.event_loop.add_event(clouds_timer)

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
        self.menu_pane = MenuPane(self.SCREEN, settings)
        self.show_pane = False

        self.button_pressed = False
        self.button_pressed_timestamp = None

        # music
        self.music_volume = self.settings.music_volume
        self.music = pg.mixer.Sound("../audio/music/Walk_the_Dinosaur_(GXSCC_Gameboy_Mix).ogg")
        self.music.set_volume(self.music_volume)
        self.music.play(loops=-1)

        # sfx
        self.sfx_volume = self.settings.sfx_volume
        self.press_start_sfx = pg.mixer.Sound("../audio/sfx/menu/king_koopa_kill_that_plumber.mp3")
        self.press_start_sfx.set_volume(self.sfx_volume)

        # easter egg - Konami Code
        self.its_a_me_sfx = pg.mixer.Sound("../audio/sfx/menu/sm64_mario_its__a_me.wav")
        self.its_a_me_sfx.set_volume(self.sfx_volume)
        self.correct_code = ["U", "U", "D", "D", "L", "R", "L", "R", "B", "A"]
        self.code_keys = []
        self.code_done = False

        # set inst_time attribute to logo object
        self.logo.inst_time = pg.time.get_ticks()

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

        self.input()

        self.check_konami_code()

        if self.code_done:
            self.its_a_me_sfx.play()
            self.code_done = False
            self.code_keys.clear()

        self.check_logo_appearance()

        self.dinohattan.update(dt)
        self.koopahari_desert.update(dt)

        if self.event_loop.loop_events() == "spawn_cloud":
            self.cloud_numb = 1 if self.cloud_numb == 2 else 2
            Cloud(group=self.clouds, cloud_numb=self.cloud_numb)

        for cloud in self.clouds:
            cloud.update(dt)

        if self.logo_appearance:
            self.logo.update(dt)

        if self.show_pane:
            self.menu_pane.update(dt)

        self.check_setting_updates()

        self.draw()


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
        self.image = pg.image.load("../graphics/title_screen/koopahari_desert.png").convert_alpha()
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
        self.image_front = pg.image.load("../graphics/title_screen/dinohattan_front.png").convert_alpha()
        self.xy_front = pg.math.Vector2(x=0, y=64)
        self.rect_front = self.image_front.get_rect(topleft = self.xy_front)
        self.image_back = pg.image.load("../graphics/title_screen/dinohattan_back.png").convert_alpha()
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
        self.image = pg.image.load("../graphics/title_screen/sky.png").convert()
        self.xy_pos = pg.math.Vector2(x=0, y=0)
        self.rect = self.image.get_rect(topleft=self.xy_pos)

    def draw(self):
        self.SCREEN.blit(self.image, self.rect)

class Cloud(pg.sprite.Sprite):
    def __init__(self, group, cloud_numb:int):
        super().__init__(group)
        self.image = pg.image.load(f"../graphics/title_screen/clouds_{cloud_numb}.png").convert_alpha()
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

class Logo:
    def __init__(self, screen):
        self.SCREEN = screen
        self.image = pg.image.load("../graphics/title_screen/logo.png").convert_alpha()
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
        self.text_surf =  font.render(text, True, (244, 244, 244))
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

class MenuPane:
    def __init__(self, screen, settings):
        self.SCREEN = screen
        self.settings = settings

        # sfx
        self.sfx_volume = self.settings.sfx_volume
        self.sfx_menu_move = pg.mixer.Sound("../audio/sfx/menu/menu_move.wav")
        self.sfx_menu_move.set_volume(self.sfx_volume)
        self.sfx_menu_pane_closing = pg.mixer.Sound("../audio/sfx/menu/screen_done.wav")
        self.sfx_menu_pane_closing.set_volume(self.sfx_volume)

        # pane graphic
        self.pane_width = 650
        self.pane_height_start = 2
        self.pane_height_end = 350
        self.pane_height_curr = self.pane_height_end
        self.xy_pos_pane = pg.math.Vector2(75, 125)
        self.load_pane()

        # font
        self.load_fonts()

        # draw attributes
        self.show_fonts = False
        self.animate_speed = 650

        # input attributes
        self.direction = pg.math.Vector2(x=0, y=1)
        self.key_pressed = True
        self.key_pressed_timestamp = pg.time.get_ticks()
        self.curr_menu_point = [0, "NEW GAME"] # starting at main menu > new_game

    def check_setting_updates(self):
        if self.sfx_volume != self.settings.sfx_volume:
            self.sfx_volume = self.settings.sfx_volume
            self.sfx_menu_move.set_volume(self.sfx_volume)
            self.sfx_menu_pane_closing.set_volume(self.sfx_volume)

    def load_fonts(self):
        # basic setup
        self.font = FONT_PRESS_START_20
        self.font_color_white = (244, 244, 244)
        self.font_color_red = (173, 26, 26)

        # menus
        # main menu (0)
        font_surf_new_game = self.font.render("NEW GAME", False, self.font_color_white)
        font_rect_new_game = font_surf_new_game.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 1)))
        font_surf_load_game = self.font.render("LOAD GAME", False, self.font_color_white)
        font_rect_load_game = font_surf_load_game.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 2)))
        font_surf_settings = self.font.render("SETTINGS", False, self.font_color_white)
        font_rect_settings = font_surf_settings.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 3)))
        font_surf_quit = self.font.render("QUIT", False, self.font_color_white)
        font_rect_quit = font_surf_quit.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 4)))

        # new game menu (1)
        # ...

        # load game menu (2)
        # ...

        # settings menu (3)
        font_surf_music_vol = self.font.render(f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%", False, self.font_color_white)
        font_rect_music_vol = font_surf_music_vol.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 1)))
        font_surf_sfx_vol = self.font.render(f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%", False, self.font_color_white)
        font_rect_sfx_vol = font_surf_sfx_vol.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 2)))
        font_surf_screen_mode = self.font.render(f"{self.settings.screen_mode}", False, self.font_color_white)
        font_rect_screen_mode = font_surf_screen_mode.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 3)))
        font_surf_back = self.font.render("BACK", False, self.font_color_white)
        font_rect_back = font_surf_back.get_rect(center = (400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 4)))

        self.fonts =  {
            0 : { # main menu
                "NEW GAME" : [font_surf_new_game, font_rect_new_game],
                "LOAD GAME" : [font_surf_load_game, font_rect_load_game],
                "SETTINGS" : [font_surf_settings, font_rect_settings],
                "QUIT" : [font_surf_quit, font_rect_quit]
            },
            1 : { # new game

            },
            2 : { # load game

            },
            3 : { # settings
                f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%" : [font_surf_music_vol, font_rect_music_vol],
                f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%" : [font_surf_sfx_vol, font_rect_sfx_vol],
                f"{self.settings.screen_mode}" : [font_surf_screen_mode, font_rect_screen_mode],
                "BACK" : [font_surf_back, font_rect_back]
            }
        }

    def load_pane(self):
        self.menu_pane_rect = pg.Rect(self.xy_pos_pane.x, self.xy_pos_pane.y, self.pane_width, self.pane_height_curr)
        self.menu_pane_surf = pg.Surface((self.pane_width, self.pane_height_curr))
        self.menu_pane_surf.fill((100, 54, 135))
        self.menu_pane_surf.set_alpha(180)

    def animate_pane(self, dt):
        if self.direction.y > 0: # window pane height increases (y=1)
            size_change = self.direction.y * self.animate_speed * dt
            if self.pane_height_curr + size_change <= self.pane_height_end:
                self.pane_height_curr += self.direction.y * self.animate_speed * dt
                self.xy_pos_pane.y -= size_change / 2
            else:
                self.direction.y = 0
        elif self.direction.y < 0: # window pane height decreases (y=-1)
            size_change = self.direction.y * self.animate_speed * dt
            if self.pane_height_curr + size_change >= self.pane_height_start:
                self.pane_height_curr += self.direction.y * self.animate_speed * dt
                self.xy_pos_pane.y -= size_change / 2
            else:
                self.direction.y = 1
        else:
            self.xy_pos_pane.y = 125
            self.show_fonts = True

    def input(self):

        if not self.key_pressed and self.show_fonts:

            def key_pressed():
                self.key_pressed = True
                self.key_pressed_timestamp = pg.time.get_ticks()

            keys = pg.key.get_pressed()

            if keys[pg.K_SPACE] or keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]:

                if self.curr_menu_point[0] == 0 or (self.curr_menu_point[0] == 3 and self.curr_menu_point[1] == "BACK"):

                    key_pressed()

                    self.direction.y = -1 # decreases pane height
                    self.sfx_menu_pane_closing.play()
                    self.show_fonts = False

                    if self.curr_menu_point[0] == 0: # main menu
                        print(f"LET'S A GO TO {self.curr_menu_point[1]}")

                        if self.curr_menu_point[1] == "QUIT":
                            pg.quit()
                            sys.exit()
                        elif self.curr_menu_point[1] == "SETTINGS":
                            self.curr_menu_point[0] = 3
                            self.curr_menu_point[1] = list(self.fonts[3].keys())[0]

                    elif self.curr_menu_point[0] == 1: # new game
                        pass

                    elif self.curr_menu_point[0] == 2: # load game
                        pass

                    elif self.curr_menu_point[0] == 3: # settings
                        self.curr_menu_point[0] = 0
                        self.curr_menu_point[1] = "SETTINGS"

            elif keys[pg.K_DOWN] or keys[pg.K_s]:

                key_pressed()

                self.sfx_menu_move.play()

                if self.curr_menu_point[0] == 0: # main menu

                    match self.curr_menu_point[1]:
                        case "NEW GAME" : self.curr_menu_point[1] = "LOAD GAME"
                        case "LOAD GAME" : self.curr_menu_point[1] = "SETTINGS"
                        case "SETTINGS" : self.curr_menu_point[1] = "QUIT"
                        case "QUIT" : self.curr_menu_point[1] = "NEW GAME"

                elif self.curr_menu_point[0] == 1: # new game
                    pass

                elif self.curr_menu_point[0] == 2: # load game
                    pass

                elif self.curr_menu_point[0] == 3: # settings

                    if self.curr_menu_point[1].startswith("MUSIC VOL."):
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[1]
                    elif self.curr_menu_point[1].startswith("SFX VOL."):
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[2]
                    elif self.curr_menu_point[1] == "WINDOW" or self.curr_menu_point[1] == "FULL SCREEN":
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[3]
                    elif self.curr_menu_point[1] == "BACK":
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[0]

            elif keys[pg.K_UP] or keys[pg.K_w]:

                key_pressed()

                self.sfx_menu_move.play()

                if self.curr_menu_point[0] == 0: # main menu

                    match self.curr_menu_point[1]:
                        case "NEW GAME" : self.curr_menu_point[1] = "QUIT"
                        case "LOAD GAME" : self.curr_menu_point[1] = "NEW GAME"
                        case "SETTINGS" : self.curr_menu_point[1] = "LOAD GAME"
                        case "QUIT" : self.curr_menu_point[1] = "SETTINGS"

                elif self.curr_menu_point[0] == 1:  # new game
                    pass

                elif self.curr_menu_point[0] == 2:  # load game
                    pass

                elif self.curr_menu_point[0] == 3:  # settings

                    if self.curr_menu_point[1].startswith("MUSIC VOL."):
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[3]
                    elif self.curr_menu_point[1].startswith("SFX VOL."):
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[0]
                    elif self.curr_menu_point[1] == "WINDOW" or self.curr_menu_point[1] == "FULL SCREEN":
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[1]
                    elif self.curr_menu_point[1] == "BACK":
                        self.curr_menu_point[1] = list(self.fonts[3].keys())[2]

            elif keys[pg.K_LEFT] or keys[pg.K_a]:

                if self.curr_menu_point[0] == 3 and self.curr_menu_point[1] != "BACK": # settings
                    key_pressed()

                    self.sfx_menu_move.play()

                    if self.curr_menu_point[1].startswith("MUSIC VOL."):
                        self.settings.decrease_volume(music_or_sfx="music")
                        self.curr_menu_point[1] = f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%"
                        self.load_fonts()

                    elif self.curr_menu_point[1].startswith("SFX VOL."):
                        self.settings.decrease_volume(music_or_sfx="sfx")
                        self.curr_menu_point[1] = f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%"
                        self.load_fonts()

                    elif self.curr_menu_point[1] == "WINDOW":
                        self.settings.screen_mode = "FULL SCREEN"
                        self.curr_menu_point[1] = self.settings.screen_mode
                        self.load_fonts()
                        self.SCREEN = self.settings.get_display_screen()

                    elif self.curr_menu_point[1] == "FULL SCREEN":
                        self.settings.screen_mode = "WINDOW"
                        self.curr_menu_point[1] = self.settings.screen_mode
                        self.load_fonts()
                        self.SCREEN = self.settings.get_display_screen()

            elif keys[pg.K_RIGHT] or keys[pg.K_d]:

                if self.curr_menu_point[0] == 3 and self.curr_menu_point[1] != "BACK": # settings
                    key_pressed()

                    self.sfx_menu_move.play()

                    if self.curr_menu_point[1].startswith("MUSIC VOL."):
                        self.settings.increase_volume(music_or_sfx="music")
                        self.curr_menu_point[1] = f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%"
                        self.load_fonts()

                    elif self.curr_menu_point[1].startswith("SFX VOL."):
                        self.settings.increase_volume(music_or_sfx="sfx")
                        self.curr_menu_point[1] = f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%"
                        self.load_fonts()

                    elif self.curr_menu_point[1] == "WINDOW":
                        self.settings.screen_mode = "FULL SCREEN"
                        self.curr_menu_point[1] = self.settings.screen_mode
                        self.load_fonts()
                        self.SCREEN = self.settings.get_display_screen()

                    elif self.curr_menu_point[1] == "FULL SCREEN":
                        self.settings.screen_mode = "WINDOW"
                        self.curr_menu_point[1] = self.settings.screen_mode
                        self.load_fonts()
                        self.SCREEN = self.settings.get_display_screen()

        else:
            if pg.time.get_ticks() - self.key_pressed_timestamp >= 400:
                self.key_pressed = False

    def update(self, dt):
        self.input()
        self.animate_pane(dt)
        self.load_pane()
        self.check_setting_updates()

    def draw_fonts(self):
        if self.show_fonts:

            # resetting all menu points back to white color
            for menu_point in self.fonts[self.curr_menu_point[0]].keys():
                self.fonts[self.curr_menu_point[0]][menu_point][0] = self.font.render(menu_point, False, self.font_color_white)

            # colorize the current menu point red
            self.fonts[self.curr_menu_point[0]][self.curr_menu_point[1]][0] = self.font.render(self.curr_menu_point[1], False, self.font_color_red)

            for font in self.fonts[self.curr_menu_point[0]].values():
                self.SCREEN.blit(font[0], font[1])

    def draw(self):
        self.SCREEN.blit(self.menu_pane_surf, self.menu_pane_rect)
        self.draw_fonts()
