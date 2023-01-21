
import pygame as pg
import math

from layers import LAYERS

class Lamp(pg.sprite.Sprite):
    def __init__(self, groups, pos, player):
        super().__init__(groups)
        self.player = player

        self.images = [pg.image.load("../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f1.png").convert_alpha(),
                       pg.image.load("../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f2.png").convert_alpha(),
                       pg.image.load("../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f3.png").convert_alpha()]
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.z = LAYERS['FG_Objects']

        self.animation_speed = 5
        self.animation_forward = True

    def check_distance_to_player(self, max_distance:int) -> bool:
        "max_distance in pixels"
        if math.dist(self.player.rect.midbottom, self.rect.center) < max_distance:
            return True
        else:
            return False

    def animate(self, dt):

        if self.animation_forward:
            next_frame = (self.animation_speed * dt) + self.frame
            if next_frame > len(self.images) - 1:
                self.animation_forward = False
                next_frame = len(self.images) - 1
        else:
            next_frame = self.frame - (self.animation_speed * dt)
            if next_frame < 0:
                self.animation_forward = True
                next_frame = 0
        self.frame = next_frame


    def update(self, dt):
        self.animate(dt)
        self.image = self.images[round(self.frame)]

