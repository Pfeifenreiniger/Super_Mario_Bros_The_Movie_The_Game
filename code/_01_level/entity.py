
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

        self.frame_index = 0
        self.run_frame_direction = 1


        self.animation_status = "stand_right"
        self.old_animation_status = self.animation_status

        self.sfx = None
        self.old_sfx_volume = self.settings.sfx_volume

        self.z = LAYERS['MG']
        self.direction = pg.math.Vector2(x=0, y=0)

        self.speed = 100
        self.gravity = 50
        self.on_floor = False

        self.collision_sprites = collision_sprites

        self.death_zones = death_zones


    def set_sfx_volume(self):
        for sfx in self.sfx.values():
            sfx.set_volume(self.settings.sfx_volume)

    def check_fall_death(self):

        if self.rect.collidelist(self.death_zones) >= 0:
            print("ENEMY DOWN!")
            self.kill()

    def check_health(self):
        if self.health <= 0:
            self.kill()

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

    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.move(dt)
        self.animate(dt)
        self.check_fall_death()
        self.check_health()
