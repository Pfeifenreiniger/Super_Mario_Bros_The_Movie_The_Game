
import pygame as pg

from code._02_level.base_loading import BaseLoading
from code._02_level.layers import LAYERS

class TrafficLight(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, pos, player, distance_between_rects_method):
        # init super classes
        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.images = (
            pg.image.load("graphics/02_streets_of_dinohattan/tileset/objects/traffic_light/traffic_light_f1.png").convert_alpha(),
            pg.image.load("graphics/02_streets_of_dinohattan/tileset/objects/traffic_light/traffic_light_f2.png").convert_alpha()
        )

        self.frame = 0
        self.image = self.images[self.frame]
        self.set_hitbox(pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.z = LAYERS['FG1']

        self.timestamp = pg.time.get_ticks()

        self.check_distance_between_rects = distance_between_rects_method

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        rect = self.image.get_rect(topleft=pos)

        margin_left = 27
        margin_top = 120
        margin_right = 167
        margin_bottom = 117

        hitbox_left = rect.left + margin_left
        hitbox_top = rect.top + margin_top

        hitbox_width = rect.width - (margin_left + margin_right)
        hitbox_height = rect.height - (margin_top + margin_bottom)

        self.rect = pg.Rect(
                            (hitbox_left,
                            hitbox_top),
                            (hitbox_width,
                            hitbox_height)
                            )

    def change_frame(self):

        # frame 0 = green for cars, red for pedestrians
        # frame 1 = red for cars, green for pedestrians
        if pg.time.get_ticks() - self.timestamp > 5000: # change traffic light every 5 seconds
            if self.frame == 0:
                self.frame = 1
                self.timestamp = pg.time.get_ticks()
            else:
                self.frame = 0
                self.timestamp = pg.time.get_ticks()
            self.image = self.images[self.frame]

    def update(self):
        self.change_frame()
