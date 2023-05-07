
import pygame as pg

from code.fonts import FONT_PRESS_START_10
from code.fader import Fader

class Cutscene:
    def __init__(self, level:int, images:tuple, texts:tuple, music, settings):
        self.settings = settings

        self.loaded = False
        self.active = False

        # image related attributes
        self.images = images
        self.img_ind = 0
        self.img_pause = False
        self.img_pause_timestamp = None
        self.image = self.images[self.img_ind]
        self.image_rect = self.image.get_rect(center=(200, 300))

        # text related attributes
        self.texts = texts
        self.font = FONT_PRESS_START_10
        self.curr_img_txt = self.texts[self.img_ind]
        self.txt_line_ind = 0
        self.curr_txt_line = self.curr_img_txt[self.txt_line_ind]
        self.char_ind = 0
        self.char_ind_copy = self.char_ind
        self.curr_text = self.curr_txt_line[:self.char_ind]
        self.y_pos_text_lines = [100]
        for i in range(len(self.curr_img_txt) - 1):
            self.y_pos_text_lines.append(self.y_pos_text_lines[-1] + 40)

        # music
        self.music = music
        music_vol = self.settings.music_volume
        self.music.set_volume(music_vol)

        self.SCREEN = self.settings.get_display_screen()

        self.fader_out = Fader(settings, "OUT")
        self.fader_in = Fader(settings, "IN")

        self.start = False
        self.end = False
        self.done = False

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True

    def turn_active(self):
        if not self.active:
            self.active = True
            self.music.play(loops=-1)

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] or keys[pg.K_RETURN] or keys[pg.K_ESCAPE] or keys[pg.K_KP_ENTER]:
            self.end = True
            self.music.fadeout(2000)

    def check_img_pause(self):
        if self.img_pause:
            if pg.time.get_ticks() - self.img_pause_timestamp > 1100:
                # as soon as the image and its text were displayed roughly about a second,
                # it flips to the next image
                self.char_ind = self.char_ind_copy = 0
                self.txt_line_ind = 0
                self.img_ind += 1
                self.image = self.images[self.img_ind]
                self.curr_img_txt = self.texts[self.img_ind]
                for i in range(len(self.curr_img_txt) - 1):
                    self.y_pos_text_lines.append(self.y_pos_text_lines[-1] + 40)

                self.img_pause = False
                self.img_pause_timestamp = None

    def check_and_update_indices(self):
        if int(self.char_ind_copy) > self.char_ind:
            if not self.char_ind + 1 >= len(self.curr_txt_line):
                self.char_ind += 1
                self.curr_text = self.curr_txt_line[:self.char_ind]
                self.char_ind_copy = self.char_ind
            else:
                if not self.txt_line_ind + 1 >= len(self.curr_img_txt):
                    self.char_ind = self.char_ind_copy = 0
                    self.txt_line_ind += 1
                    self.curr_txt_line = self.texts[self.img_ind][self.txt_line_ind]
                else:
                    if not self.img_ind + 1 >= len(self.images):
                        self.img_pause = True
                        self.img_pause_timestamp = pg.time.get_ticks()
                    else:
                        self.end = True
                        self.music.fadeout(2000)

    def draw(self):

        # black bg
        self.SCREEN.fill((0, 0, 0))

        # image
        self.SCREEN.blit(self.image, self.image_rect)

        # text
        for i in range(self.txt_line_ind + 1):
            if i == self.txt_line_ind:
                text_surf = self.font.render(self.texts[self.img_ind][i][:self.char_ind+1], False, (244, 244, 244))
            else:
                text_surf = self.font.render(self.texts[self.img_ind][i], False, (244, 244, 244))

            text_rect = text_surf.get_rect(topleft=(394, self.y_pos_text_lines[i]))

            self.SCREEN.blit(text_surf, text_rect)

        # fade out if end
        if self.end:
            self.fade_out()


    def fade_in(self):
        if self.fader_in.alpha_value > 0:
            self.fader_in.update()
            self.fader_in.draw()
        else:
            self.start = True

    def fade_out(self):
        if self.fader_out.alpha_value < 255:
            self.fader_out.update()
            self.fader_out.draw()
        else:
            self.music.stop()
            self.done = True

    def update(self, dt):

        if self.start:

            self.check_img_pause()

            self.input()

            if not self.end and not self.img_pause:
                self.char_ind_copy += 20 * dt
                self.check_and_update_indices()

            self.draw()

        else:

            self.fade_in()


class Intro(Cutscene):
    def __init__(self, level:int, settings):

        self.lvl = level
        self.load_images()
        self.load_texts()
        self.load_music()

        super().__init__(level=self.lvl, images=self.images, texts=self.texts, music=self.music, settings=settings)

    def load_images(self):

        self.images:tuple

        if self.lvl == 1:
            self.images = (
                pg.image.load("graphics/01_excavation_site/intro/01_intro_01.png").convert(),
                pg.image.load("graphics/01_excavation_site/intro/01_intro_02.png").convert(),
                pg.image.load("graphics/01_excavation_site/intro/01_intro_03.png").convert(),
                pg.image.load("graphics/01_excavation_site/intro/01_intro_04.png").convert()
            )

    def load_texts(self):

        self.texts:tuple

        if self.lvl == 1:
            self.texts = (("Not so long ago, in a place known as", # 01_intro_01
                           "Brooklyn, there lived a young woman,",
                           "named Daisy.",
                           "Daisy was an archaeologist -",
                           "a person who studies the past by",
                           "digging for remains that have long",
                           "been buried. Daisy always wore a",
                           "crystal pendant around her neck.",
                           "She didn't knew it, but she was",
                           "really a princess from another world.",
                           "Her pendant was the only thing, that",
                           "could bring the two worlds together."),
                          ("Meanwhile, in the other world, an", # 01_intro_02
                           "evil man named Koopa was making plans.",
                           "With him were Iggy and Spike, his",
                           "loyal followers. Koopa knew all about",
                           'Princess Daisy. "I want you guys to',
                           'find the princess and bring her to me,"',
                           'said Kopa. "I need her crystal to unite',
                           "our world with the Earth. Then I will",
                           "rule both worlds!",
                           'Get me the princess!" he ordered.'),
                          ("Back on Earth, Daisy discovered", # 01_intro_03
                           "that the tunnel in which she had been",
                           "digging was quickly filling up with",
                           "water. She called her two friends,",
                           "Mario Mario and Luigi Mario,",
                           "the best plumbers in Brooklyn."),
                          ("In the tunnel, Daisy and the Mario", # 01_intro_04
                           "brothers discovered they weren't alone.",
                           "Iggy and Spike were there waiting!",
                           "The evil pair grabbed Daisy and dragged",
                           "her toward a gateway to the other world.",
                           '"Let go of me!" Daisy yelled...')
            )

    def load_music(self):

        if self.lvl == 1:
            self.music = pg.mixer.Sound("audio/music/HeatleyBros - 8 Bit Town.mp3")


class Outro(Cutscene):
    def __init__(self, level:int, settings):
        self.lvl = level
        self.load_images()
        self.load_texts()
        self.load_music()

        super().__init__(level=self.lvl, images=self.images, texts=self.texts, music=self.music, settings=settings)

    def load_images(self):

        if self.lvl == 1:
            self.images = (
                pg.image.load("graphics/01_excavation_site/outro/01_outro_01.png").convert(),
            )

    def load_texts(self):

        if self.lvl == 1:
            self.texts = (("Luigi and Mario watched in horror as",
                           "Daisy disappeared through the gateway.",
                           "Luigi tried to grab her, but he caught",
                           "only the crystal hanging from her neck.",
                           '"We must save Daisy!" cried Luigi.'),
            )

    def load_music(self):

        if self.lvl == 1:
            self.music = pg.mixer.Sound("audio/music/Dawid Podsiadło - Let You Down (Chiptune Mix by Sammeh12 8-bit).mp3")
