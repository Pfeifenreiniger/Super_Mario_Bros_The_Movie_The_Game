
import pygame as pg
import random as rnd

from math import sin

from code._02_level.base_loading import BaseLoading
from code._02_level.humanoid import Humanoid, HumanoidShadow
from code._02_level.layers import LAYERS

class Player(Humanoid):
    def __init__(self, groups, pos, collision_sprites, map_width, map_height, settings, menu_pane, distance_between_rects_method, end_zone):

        self.sprites = {
            "stand_left" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_left/player_stand_left_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_left/player_stand_left_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_left/player_stand_left_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_left/player_stand_left_f4.png").convert_alpha()
            ),
            "stand_right" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_right/player_stand_right_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_right/player_stand_right_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_right/player_stand_right_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_right/player_stand_right_f4.png").convert_alpha()
            ),
            "stand_up" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_up/player_stand_up_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_up/player_stand_up_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_up/player_stand_up_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_up/player_stand_up_f4.png").convert_alpha()
            ),
            "stand_down" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_down/player_stand_down_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_down/player_stand_down_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_down/player_stand_down_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/stand_down/player_stand_down_f4.png").convert_alpha()
            ),
            "run_left" : (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f4.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f5.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f6.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f7.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_left/player_run_left_f8.png").convert_alpha()
            ),
            "run_right": (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f4.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f5.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f6.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f7.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_right/player_run_right_f8.png").convert_alpha()
            ),
            "run_up": (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f4.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f5.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f6.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f7.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_up/player_run_up_f8.png").convert_alpha()
            ),
            "run_down": (
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f1.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f2.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f3.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f4.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f5.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f6.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f7.png").convert_alpha(),
                pg.image.load("graphics/02_streets_of_dinohattan/entities/player/run_down/player_run_down_f8.png").convert_alpha()
            ),
            "shadows" : {
                "big" : pg.image.load("graphics/02_streets_of_dinohattan/entities/player/shadows/player_shadow_big.png").convert_alpha(),
                "small" : pg.image.load("graphics/02_streets_of_dinohattan/entities/player/shadows/player_shadow_small.png").convert_alpha()
            }
        }

        self.image = self.sprites["stand_up"][0]

        super().__init__(groups=groups,
                         pos=pos,
                         collision_sprites=collision_sprites,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.shadow = PlayerShadow(groups=groups,
                                   x_pos=self.xy_pos.x,
                                   y_pos=self.xy_pos.y,
                                   distance_between_rects_method=distance_between_rects_method)

        self.start_arrow = StartArrow(groups=groups,
                                      x_pos=self.rect.centerx - 54,
                                      y_pos=self.rect.centery - 300,
                                      distance_between_rects_method=distance_between_rects_method)

        self.speed = 130
        self.max_health = self.health
        self.lives = 3
        self.dead = False
        self.is_vulnerable = True
        self.invul_duration = 1500
        self.hit_time = None

        self.menu_pane = menu_pane
        self.menu_pressed = False
        self.menu_pressed_timestamp = None

        self.end_zone = end_zone

        # sfx
        self.sfx_volume = self.settings.sfx_volume
        self.lose_life_sfx = pg.mixer.Sound("audio/sfx/player/lose_life.mp3")
        self.lose_life_sfx.set_volume(self.sfx_volume)

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = self.image.get_rect(topleft=pos)

        hitbox_margin = int((self.rect.width / 5))
        hitbox_left = self.rect.left + hitbox_margin
        hitbox_top = self.rect.top + hitbox_margin

        self.rect = pg.Rect((hitbox_left,  # left
                               hitbox_top), # top
                              (self.rect.width - (2 * hitbox_margin),  # width
                               self.rect.height - (2 * hitbox_margin))) # height

    def input(self):

        if self.start_arrow.is_done:

            if not self.menu_pane.active:

                keys = pg.key.get_pressed()

                # horizontal movement
                if keys[pg.K_RIGHT]:
                    self.direction.x = 1
                    self.animation_status = "run_right"

                elif keys[pg.K_LEFT]:
                    self.direction.x = -1
                    self.animation_status = "run_left"

                else:
                    self.direction.x = 0

                # vertical movement
                if keys[pg.K_UP]:
                    self.direction.y = -1
                    self.animation_status = "run_up"

                elif keys[pg.K_DOWN]:
                    self.direction.y = 1
                    self.animation_status = "run_down"

                else:
                    self.direction.y = 0

                # activate menu pane
                if keys[pg.K_ESCAPE] and not self.menu_pressed:
                    self.direction.x = 0
                    self.direction.y = 0

                    self.menu_pane.active = True
                    self.menu_pane.key_pressed = True
                    self.menu_pane.key_pressed_timestamp = pg.time.get_ticks()

                    self.menu_pressed = True
                    self.menu_pressed_timestamp = pg.time.get_ticks()

                if self.menu_pressed:
                    if pg.time.get_ticks() - self.menu_pressed_timestamp > 300:
                        self.menu_pressed = False


    def check_collision(self, direction):

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 90 pixels distance to player
            if sprite.check_distance_between_rects(rect1=self.rect, rect2=sprite.hitbox, max_distance=1000):

                if direction == 'horizontal':
                    if sprite.hitbox.colliderect(self.rect):
                        # left collision
                        if self.direction.x < 0:
                            if self.rect.left <= sprite.hitbox.right:
                                self.rect.left = sprite.hitbox.right
                        # right collision
                        elif self.direction.x > 0:
                            if self.rect.right >= sprite.hitbox.left:
                                self.rect.right = sprite.hitbox.left

                        self.xy_pos.x = self.rect.x

                elif direction == "vertical":
                    if sprite.hitbox.colliderect(self.rect):
                        # top collision
                        if self.direction.y < 0:
                            if self.rect.top <= sprite.hitbox.bottom:
                                self.rect.top = sprite.hitbox.bottom
                        # bottom collision
                        elif self.direction.y > 0:
                            if self.rect.bottom >= sprite.hitbox.top:
                                self.rect.bottom = sprite.hitbox.top

                        self.xy_pos.y = self.rect.y

    def check_end_zone(self):
        # if contact to level end zone -> returns True
        if self.rect.colliderect(self.end_zone):
            return True
        else:
            return False

    def move(self, dt):
        """player checks collision to level objects"""

        # normalize a vector -> length of vector is going to be 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()


        # horizontal movement
        x_movement = self.direction.x * self.speed * dt

        # horizontal movement only possible between horizontal level edges
        if self.xy_pos.x + x_movement > 0 and self.xy_pos.x + x_movement < self.map_width - self.rect.width:
            self.xy_pos.x += x_movement

        self.rect.x = round(self.xy_pos.x)
        self.check_collision('horizontal')

        # vertical movement
        y_movement = self.direction.y * self.speed * dt

        # vertical movement only possible between vertical level edges
        if self.xy_pos.y - y_movement > 0 and self.xy_pos.y + y_movement < self.map_height - self.rect.height:
            self.xy_pos.y += y_movement

        self.rect.y = round(self.xy_pos.y)
        self.check_collision('vertical')

    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pg.time.get_ticks()
            if current_time - self.hit_time > self.invul_duration:
                self.is_vulnerable = True

    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pg.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False

    def lose_life(self):

        if self.is_vulnerable:
            self.hit_time = pg.time.get_ticks()
            self.is_vulnerable = False
            self.lives -= 1
            self.lose_life_sfx.play()
            if self.lives <= 0:
                self.dead = True

    def get_pushed(self, pusher_hitbox):
        if pusher_hitbox.bottom > self.rect.bottom:
            self.rect.bottom = pusher_hitbox.top - 1
        elif pusher_hitbox.top < self.rect.top:
            self.rect.top = pusher_hitbox.bottom + 1
        else:
            if rnd.randint(0, 1) == 0:
                self.rect.bottom = pusher_hitbox.top - 1
            else:
                self.rect.top = pusher_hitbox.bottom + 1

        self.xy_pos.x = self.rect.x
        self.xy_pos.y = self.rect.y

    def update_shadow(self):

        if "run" in self.animation_status:
            if int(self.frame_index) == 0 or int(self.frame_index) == len(self.sprites[self.animation_status]) - 1:
                self.shadow.change_size(to='big')
            else:
                if self.shadow.size == 'big':
                    self.shadow.change_size(to='small')
        else:
            if self.shadow.size == 'big':
                self.shadow.change_size(to='small')

        self.shadow.update_xy_pos(x=self.xy_pos.x, y=self.xy_pos.y)

    def check_sfx_vol(self):
        if self.sfx_volume != self.settings.sfx_volume:
            self.sfx_volume = self.settings.sfx_volume
            self.lose_life_sfx.set_volume(self.sfx_volume)

    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.input()
        self.is_idle_animation()
        self.move(dt)
        self.animate(dt)
        self.update_shadow()
        self.vulnerability_timer()
        self.blink()
        self.check_sfx_vol()


class PlayerShadow(HumanoidShadow):
    def __init__(self, groups, x_pos:int, y_pos:int, distance_between_rects_method):

        self.sprites = {
            'big' : pg.image.load("graphics/02_streets_of_dinohattan/entities/player/shadows/player_shadow_big.png").convert_alpha(),
            'small' : pg.image.load("graphics/02_streets_of_dinohattan/entities/player/shadows/player_shadow_small.png").convert_alpha()
        }

        super().__init__(
            groups=groups,
            sprites=self.sprites,
            x_pos=x_pos,
            y_pos=y_pos,
            xy_pos_margin=-5,
            distance_between_rects_method=distance_between_rects_method
        )

        self.size = 'small'



class StartArrow(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, x_pos, y_pos, distance_between_rects_method):

        self.is_init = False

        self.image = pg.image.load("graphics/02_streets_of_dinohattan/entities/player/start_arrow/start_arrow.png").convert_alpha()

        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.xy_pos = pg.math.Vector2(x=x_pos, y=y_pos)
        self.rect = self.image.get_rect(topleft=self.xy_pos)

        self.z = LAYERS['FG4']

        self.is_visible = True
        self.blink_timestamp = None
        self.init_timestamp = None
        self.is_done = False

        self.check_distance_between_rects = distance_between_rects_method

    def init_timestamps(self):
        if self.is_init:
            self.blink_timestamp = pg.time.get_ticks()
            self.init_timestamp = self.blink_timestamp

    def blink(self):

        if pg.time.get_ticks() - self.blink_timestamp > 800:
            self.is_visible = True if self.is_visible == False else False
            self.blink_timestamp = pg.time.get_ticks()

    def check_if_done(self):
        if pg.time.get_ticks() - self.init_timestamp > 5500:
            self.is_done = True
            self.kill()

    def update(self):

        if self.init_timestamp != None:
            self.check_if_done()

        if self.blink_timestamp != None:
            self.blink()
