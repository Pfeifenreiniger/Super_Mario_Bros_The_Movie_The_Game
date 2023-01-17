
import pygame as pg

from layers import LAYERS

class Player(pg.sprite.Sprite):
    def __init__(self, groups, pos, collision_sprites, map_width):
        super().__init__(groups)

        self.image = pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.start_xy_pos = self.xy_pos
        self.z = LAYERS['MG']
        self.direction = pg.math.Vector2(x=0, y=0)
        self.speed = 250
        self.jump_speed = 600
        self.gravity = 50
        self.on_floor = False

        self.jumped = False

        # collision
        self.collision_sprites = collision_sprites

        self.map_width = map_width


    def check_floor_contact(self):

        bottom_rect = pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 40)

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 200 pixels distance to player
            if sprite.check_distance_to_player(60):

                # contact between player and floor
                if sprite.rect.colliderect(self.rect):

                    if self.rect.bottom >= sprite.rect.top:
                        self.direction.y = 0
                        self.on_floor = True
                        if self.jumped:
                            self.jumped = False
                        self.rect.bottom = sprite.rect.top
                        self.xy_pos = pg.math.Vector2(self.rect.topleft)
                        contact = True
                        break
                else:
                    contact = True

        # no contact between player and floor and not jumping -> falling
        if not contact and not self.jumped:
            self.on_floor = False
            self.direction.x = 0

    def input(self):

        keys = pg.key.get_pressed()

        if self.on_floor or self.jumped:
            # horizontal input
            if keys[pg.K_RIGHT]:
                self.direction.x = 1
            elif keys[pg.K_LEFT]:
                self.direction.x = -1
            else:
                self.direction.x = 0

        if not self.jumped:
            # vertical input (jumping)
            if keys[pg.K_UP] or keys[pg.K_SPACE]:
                self.direction.y -= self.jump_speed
                self.on_floor = False
                self.jumped = True

    def move(self, dt):

        # horizontal movement
        x_movement = self.direction.x * self.speed * dt

        if self.xy_pos.x + x_movement > 0 and self.xy_pos.x + x_movement < self.map_width - self.rect.width:
            self.xy_pos.x += x_movement

        self.rect.x = round(self.xy_pos.x)


        # vertical movement
        if not self.on_floor:
            self.direction.y += self.gravity
        self.xy_pos.y += self.direction.y * dt
        self.rect.y = round(self.xy_pos.y)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.check_floor_contact()
        self.input()
        self.move(dt)
        # print("current rect", self.rect.left)
        # print("old rect", self.old_rect.left)


