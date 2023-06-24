
import pygame as pg

from code._02_level.base_loading import BaseLoading
from code._02_level.layers import LAYERS

class Entity(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, pos, settings, map_width, map_height, distance_between_rects_method):
        # init super classes
        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.settings = settings
        self.map_width = map_width
        self.map_height = map_height

        self.check_distance_between_rects = distance_between_rects_method

        self.set_hitbox(pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.start_xy_pos = tuple(self.xy_pos)

        self.z = LAYERS['MG']

        self.direction = pg.math.Vector2(x=0, y=0)
        self.speed = 100

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = pg.Rect((pos[0],  # left
                             pos[1]),  # top
                            (50,  # width
                             50))  # height
        self.hitbox = self.rect

    def move(self, dt):

        # normalize a vector -> length of vector is going to be 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


        # horizontal movement
        x_movement = self.direction.x * self.speed * dt

        self.xy_pos.x += x_movement

        self.hitbox.x = round(self.xy_pos.x)

        # vertical movement
        y_movement = self.direction.y * self.speed * dt

        self.xy_pos.y += y_movement

        self.hitbox.y = round(self.xy_pos.y)

