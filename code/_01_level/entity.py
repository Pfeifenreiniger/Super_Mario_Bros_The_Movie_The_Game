
import pygame as pg
from code._01_level.layers import LAYERS

class Entity(pg.sprite.Sprite):
    def __init__(self, groups, pos, collision_sprites, death_zones, settings, map_width, distance_between_rects_method):
        super().__init__(groups)

        self.loaded = False

        self.settings = settings
        self.map_width = map_width
        self.check_distance_between_rects = distance_between_rects_method

        self.health = 100
        self.attack_power = 10

        self.frame_index = 0
        self.run_frame_direction = 1

        self.animation_status = "stand_right"
        self.old_animation_status = self.animation_status

        self.set_hitbox(pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.start_xy_pos = tuple(self.xy_pos)

        self.sfx = {}
        self.old_sfx_volume = self.settings.sfx_volume

        self.z = LAYERS['MG']
        self.direction = pg.math.Vector2(x=0, y=0)

        self.speed = 100
        self.gravity = 50
        self.on_floor = False

        self.collision_sprites = collision_sprites

        self.death_zones = death_zones

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = pg.Rect((pos[0],  # left
                             pos[1]),  # top
                            (50,  # width
                             50))  # height

    def set_sfx_volume(self):
        for sfx in self.sfx.values():
            sfx.set_volume(self.settings.sfx_volume)




    def move(self, dt):

        # horizontal movement
        x_movement = self.direction.x * self.speed * dt

        # horizontal movement only possible between outer level edges
        if self.xy_pos.x + x_movement > 0 and self.xy_pos.x + x_movement < self.map_width - self.rect.width:
            self.xy_pos.x += x_movement

        self.rect.x = round(self.xy_pos.x)
        self.check_collision('horizontal')


        # vertical movement
        if not self.on_floor:
            self.direction.y += self.gravity
        self.xy_pos.y += self.direction.y * dt
        self.rect.y = round(self.xy_pos.y)
        self.check_collision('vertical')

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True
