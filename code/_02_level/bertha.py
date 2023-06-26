
import pygame as pg

from code._02_level.base_loading import BaseLoading
from code._02_level.humanoid import Humanoid, HumanoidShadow
from code._02_level.layers import LAYERS

class Bertha(Humanoid):
    def __init__(self, groups, pos, collision_sprites, map_width, map_height, settings, distance_between_rects_method):

        self.is_init = False

        self.sprites = {
            "run_up" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f4.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f5.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f6.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f7.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/run_up/bertha_run_up_f8.png").convert_alpha(),
            ),
            "shadows": {
                "big": pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/shadows/bertha_shadow_big.png").convert_alpha(),
                "small": pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/shadows/bertha_shadow_small.png").convert_alpha()
            }
        }

        self.image = self.sprites["run_up"][0]

        super().__init__(groups=groups,
                         pos=pos,
                         collision_sprites=collision_sprites,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.direction.y = -1
        self.animation_status = "run_up"
        self.old_animation_status = "run_up"

        self.shadow = BerthaShadow(groups=groups,
                                   x_pos=self.xy_pos.x,
                                   y_pos=self.xy_pos.y,
                                   distance_between_rects_method=distance_between_rects_method)

        self.speed = 140

    def update_shadow(self):

        if int(self.frame_index) == 0 or int(self.frame_index) == len(self.sprites[self.animation_status]) - 1:
            self.shadow.change_size(to='big')
        else:
            if self.shadow.size == 'big':
                self.shadow.change_size(to='small')

        self.shadow.update_xy_pos(x=self.xy_pos.x, y=self.xy_pos.y)

    def check_vanish(self):
        if self.xy_pos.y < 3000:
            self.shadow.kill()
            self.kill()

    def update(self, dt):
        if self.is_init:
            self.move(dt)
            self.update_shadow()
            self.animate(dt)
            self.check_vanish()


class BerthaShadow(HumanoidShadow):
    def __init__(self, groups, x_pos:int, y_pos:int, distance_between_rects_method):

        self.sprites = {
            'big' : pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/shadows/bertha_shadow_big.png").convert_alpha(),
            'small': pg.image.load("graphics/02_streets_of_dinohattan/entities/bertha/shadows/bertha_shadow_small.png").convert_alpha(),
        }

        super().__init__(
            groups=groups,
            sprites=self.sprites,
            x_pos=x_pos,
            y_pos=y_pos,
            xy_pos_margin=3,
            distance_between_rects_method=distance_between_rects_method
        )

        self.size = 'big'
