
import pygame as pg

from code._02_level.base_loading import BaseLoading
from code._02_level.layers import LAYERS

class TrafficLight(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, pos, player, distance_between_rects_method):
        # init super classes
        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.images = [
            pg.image.load("graphics/02_streets_of_dinohattan_tileset/objects/traffic_light/traffic_light_f1.png").convert_alpha(),
            pg.image.load("graphics/02_streets_of_dinohattan_tileset/objects/traffic_light/traffic_light_f2.png").convert_alpha()
        ]

        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.z = LAYERS['FG1']

        self.timestamp = pg.time.get_ticks()

        self.check_distance_between_rects = distance_between_rects_method

    def change_frame(self):

        # frame 0 = green for cars, red for pedestrians
        # frame 1 = red for cars, green for pedestrians
        if pg.time.get_ticks() - self.timestamp > 5000:
            if self.frame == 0:
                self.frame = 1
            else:
                self.frame = 0
            self.image = self.images[self.frame]

    def update(self):
        self.change_frame()
