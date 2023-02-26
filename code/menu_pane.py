
import pygame as pg
import sys

from fonts import FONT_MASHEEN_BOLD_30, FONT_PRESS_START_20

class MenuPane:
    def __init__(self, screen, settings, locator):
        self.SCREEN = screen
        self.settings = settings
        self.locator = locator

        self.active = False

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


        if self.locator.current_location == 0:
            self.curr_menu_point = [0, "NEW GAME"] # starting at main menu > new_game
        else:
            self.curr_menu_point = [0, "CONTINUE"] # starting at main menu > continue

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
        if self.locator.current_location == 0: # title menu
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

        else: # pause menu

            # main menu (0)
            font_surf_continue = self.font.render("CONTINUE", False, self.font_color_white)
            font_rect_continue = font_surf_continue.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 4) * 1)))

            font_surf_quit = self.font.render("QUIT", False, self.font_color_white)
            font_rect_quit = font_surf_quit.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 4) * 2)))

            font_surf_settings = self.font.render("SETTINGS", False, self.font_color_white)
            font_rect_settings = font_surf_settings.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 4) * 3)))

            # settings menu (1)
            font_surf_music_vol = self.font.render(f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%", False, self.font_color_white)
            font_rect_music_vol = font_surf_music_vol.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 1)))

            font_surf_sfx_vol = self.font.render(f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%", False, self.font_color_white)
            font_rect_sfx_vol = font_surf_sfx_vol.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 2)))

            font_surf_screen_mode = self.font.render(f"{self.settings.screen_mode}", False, self.font_color_white)
            font_rect_screen_mode = font_surf_screen_mode.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 3)))

            font_surf_back = self.font.render("BACK", False, self.font_color_white)
            font_rect_back = font_surf_back.get_rect(center=(400, self.xy_pos_pane.y + round((self.pane_height_end / 5) * 4)))

            self.fonts = {
                0: {  # main menu
                    "CONTINUE": [font_surf_continue, font_rect_continue],
                    "QUIT": [font_surf_quit, font_rect_quit],
                    "SETTINGS": [font_surf_settings, font_rect_settings]
                },
                1: {  # settings
                    f"MUSIC VOL.: {int(self.settings.music_volume * 100)}%": [font_surf_music_vol, font_rect_music_vol],
                    f"SFX VOL.: {int(self.settings.sfx_volume * 100)}%": [font_surf_sfx_vol, font_rect_sfx_vol],
                    f"{self.settings.screen_mode}": [font_surf_screen_mode, font_rect_screen_mode],
                    "BACK": [font_surf_back, font_rect_back]
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

                if self.locator.current_location == 0: # title menu

                    if self.curr_menu_point[0] == 0 or (self.curr_menu_point[0] == 3 and self.curr_menu_point[1] == "BACK"):

                        key_pressed()

                        self.direction.y = -1 # decreases pane height
                        self.sfx_menu_pane_closing.play()
                        self.show_fonts = False

                        if self.curr_menu_point[0] == 0: # main menu
                            print(f"LET'S A GO TO {self.curr_menu_point[1]}")

                            if self.curr_menu_point[1] == "NEW GAME":
                                self.active = False
                                self.locator.current_location = 1
                            elif self.curr_menu_point[1] == "QUIT":
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

                else: # pause menu

                    if self.curr_menu_point[0] == 0 or (self.curr_menu_point[0] == 1 and self.curr_menu_point[1] == "BACK"):

                        key_pressed()

                        self.direction.y = -1

                        self.sfx_menu_pane_closing.play()
                        self.show_fonts = False

                        if self.curr_menu_point[0] == 0:

                            if self.curr_menu_point[1] == "CONTINUE":
                                self.active = False

                            elif self.curr_menu_point[1] == "QUIT":
                                self.locator.current_location = 0

                            elif self.curr_menu_point[1] == "SETTINGS":
                                self.curr_menu_point[0] = 1
                                self.curr_menu_point[1] = list(self.fonts[1].keys())[0]

                        elif self.curr_menu_point[0] == 1:
                            self.curr_menu_point[0] = 0
                            self.curr_menu_point[1] = "SETTINGS"

            elif keys[pg.K_DOWN] or keys[pg.K_s]:

                key_pressed()

                self.sfx_menu_move.play()

                if self.locator.current_location == 0: # title menu

                    if self.curr_menu_point[0] == 0: # main menu

                        match self.curr_menu_point[1]:
                            case "NEW GAME" : self.curr_menu_point[1] = "LOAD GAME"
                            case "LOAD GAME" : self.curr_menu_point[1] = "SETTINGS"
                            case "SETTINGS" : self.curr_menu_point[1] = "QUIT"
                            case "QUIT" : self.curr_menu_point[1] = "NEW GAME"

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

                else: # pause menu

                    if self.curr_menu_point[0] == 0:

                        match self.curr_menu_point[1]:
                            case "CONTINUE" : self.curr_menu_point[1] = "QUIT"
                            case "QUIT" : self.curr_menu_point[1] = "SETTINGS"
                            case "SETTINGS" : self.curr_menu_point[1] = "CONTINUE"

                    elif self.curr_menu_point[0] == 1:  # settings

                        if self.curr_menu_point[1].startswith("MUSIC VOL."):
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[1]
                        elif self.curr_menu_point[1].startswith("SFX VOL."):
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[2]
                        elif self.curr_menu_point[1] == "WINDOW" or self.curr_menu_point[1] == "FULL SCREEN":
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[3]
                        elif self.curr_menu_point[1] == "BACK":
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[0]

            elif keys[pg.K_UP] or keys[pg.K_w]:

                key_pressed()

                self.sfx_menu_move.play()

                if self.locator.current_location == 0: # title menu

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

                else: # pause menu

                    if self.curr_menu_point[0] == 0:

                        match self.curr_menu_point[1]:
                            case "CONTINUE" : self.curr_menu_point[1] = "SETTINGS"
                            case "QUIT" : self.curr_menu_point[1] = "CONTINUE"
                            case "SETTINGS" : self.curr_menu_point[1] = "QUIT"

                    elif self.curr_menu_point[0] == 1:  # settings

                        if self.curr_menu_point[1].startswith("MUSIC VOL."):
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[3]
                        elif self.curr_menu_point[1].startswith("SFX VOL."):
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[0]
                        elif self.curr_menu_point[1] == "WINDOW" or self.curr_menu_point[1] == "FULL SCREEN":
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[1]
                        elif self.curr_menu_point[1] == "BACK":
                            self.curr_menu_point[1] = list(self.fonts[1].keys())[2]

            elif keys[pg.K_LEFT] or keys[pg.K_a]:

                if (self.locator.current_location == 0 and self.curr_menu_point[0] == 3 and self.curr_menu_point[1] != "BACK") \
                    or (self.locator.current_location != 0 and self.curr_menu_point[0] == 1 and self.curr_menu_point[1] != "BACK"): # settings
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

                if (self.locator.current_location == 0 and self.curr_menu_point[0] == 3 and self.curr_menu_point[1] != "BACK") \
                    or (self.locator.current_location != 0 and self.curr_menu_point[0] == 1 and self.curr_menu_point[1] != "BACK"): # settings
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

        if self.active:
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
        if self.active:
            self.SCREEN.blit(self.menu_pane_surf, self.menu_pane_rect)
            self.draw_fonts()

