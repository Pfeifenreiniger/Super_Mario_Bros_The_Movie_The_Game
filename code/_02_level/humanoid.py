
import pygame as pg

from code._02_level.base_loading import BaseLoading
from code._02_level.entity import Entity
from code._02_level.layers import LAYERS

class Humanoid(Entity):
    def __init__(self, groups, pos, collision_sprites, settings, map_width, map_height, distance_between_rects_method):
        super().__init__(groups=groups,
                         pos=pos,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.health = 100

        self.frame_index = 0
        self.frame_rotation_power = 7

        self.animation_status = "stand_up"
        self.old_animation_status = self.animation_status

        self.run_frame_direction = 1

        self.collision_sprites = collision_sprites

    def is_idle_animation(self):
        if self.direction.x == 0 and self.direction.y == 0 and not 'stand' in self.animation_status:
            if 'up' in self.animation_status:
                self.animation_status = 'stand_up'
            elif 'down' in self.animation_status:
                self.animation_status = 'stand_down'
            elif 'left' in self.animation_status:
                self.animation_status = 'stand_left'
            elif 'right' in self.animation_status:
                self.animation_status = 'stand_right'

    def check_frame_rotation_power(self):
        if "run" in self.animation_status:
            self.frame_rotation_power = 9
        else:
            self.frame_rotation_power = 6

    def animate(self, dt):

        self.check_frame_rotation_power()

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if "run" in self.animation_status:

            if self.run_frame_direction > 0:  # going forward through tuple
                self.frame_index += self.frame_rotation_power * dt
                if self.frame_index >= len(self.sprites[self.animation_status]):
                    self.frame_index = len(self.sprites[self.animation_status]) - 1
                    self.run_frame_direction = -1
            else:  # going backwards through tuple
                self.frame_index -= self.frame_rotation_power * dt
                if self.frame_index < 0:
                    self.frame_index = 0
                    self.run_frame_direction = 1

        else:
            self.frame_index += self.frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites[self.animation_status]):
                self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]


class HumanoidShadow(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, sprites, x_pos:int, y_pos:int, xy_pos_margin:int, distance_between_rects_method):

        self.sprites = sprites

        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.size = 'small'

        self.xy_pos = pg.math.Vector2(x_pos, y_pos)
        self.xy_pos_margin = xy_pos_margin
        self.z = LAYERS['BG2']

        self.image = self.sprites[self.size]
        self.rect = self.image.get_rect(topleft=self.xy_pos)

        self.check_distance_between_rects = distance_between_rects_method

    def update_xy_pos(self, x, y):

        self.xy_pos.x = x + self.xy_pos_margin
        self.xy_pos.y = y + self.xy_pos_margin
        self.rect.x = round(self.xy_pos.x)
        self.rect.y = round(self.xy_pos.y)

    def change_size(self, to:str):
        """
        to = 'small' or 'big'
        """

        self.size = to.lower()
        self.image = self.sprites[self.size]
