
import pygame as pg

from code._02_level.entity import Entity
from code._02_level.layers import LAYERS

class Train(Entity):
    def __init__(self, groups, surf, pos, map_width, map_height, settings, distance_between_rects_method):

        self.rotate_image(image=surf, angle=163.04)

        super().__init__(groups=groups,
                         pos=pos,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.z = LAYERS['FG4']

        self.direction.x = 1
        self.direction.y = 1
        self.speed_x = 380
        self.speed_y = self.speed_x * 0.3025 # speed_y round about 30% of speed_x

    def rotate_image(self, image, angle):

        self.image = pg.transform.rotate(image, angle)

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = pg.Rect((pos[0],  # left
                             pos[1]),  # top
                            (self.image.get_width(),  # width
                             self.image.get_height()))  # height

    def move(self, dt):

        # normalize a vector -> length of vector is going to be 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


        # horizontal movement
        x_movement = self.direction.x * self.speed_x * dt

        self.xy_pos.x += x_movement

        self.rect.x = round(self.xy_pos.x)

        # vertical movement
        y_movement = self.direction.y * self.speed_y * dt

        self.xy_pos.y += y_movement

        self.rect.y = round(self.xy_pos.y)

    def check_restart_pos(self):
        if self.rect.left > self.map_width:
            self.xy_pos.x = self.start_xy_pos[0]
            self.xy_pos.y = self.start_xy_pos[1]
            self.rect.topleft = self.xy_pos

    def update(self, dt):
        self.move(dt)
        self.check_restart_pos()
