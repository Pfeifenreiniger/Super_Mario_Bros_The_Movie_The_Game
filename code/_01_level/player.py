
import pygame as pg

from layers import LAYERS

class Player(pg.sprite.Sprite):
    def __init__(self, groups, pos, collision_sprites, map_width, death_zones):
        super().__init__(groups)

        self.sprites = {
            "stand_left" : (pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha(),
                            pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha()),
            "stand_right" : (pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha(),
                             pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha()),
            "run_left" : (pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f1.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f2.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f3.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f4.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f5.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f6.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f7.png").convert_alpha(),
                          pg.image.load("../graphics/01_excavation_site/entities/player/run_left/player_run_left_f8.png").convert_alpha()),
            "run_right" : (pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f1.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f2.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f3.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f4.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f5.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f6.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f7.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/run_right/player_run_right_f8.png").convert_alpha()),
            "jump_left" : (pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha(),
                           pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha()),
            "jump_right" : (pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha(),
                            pg.image.load("../graphics/01_excavation_site/entities/player/player_test.png").convert_alpha())
        }
        self.frame_index = 0
        self.run_frame_direction = 1
        self.animation_status = "stand_right"
        self.old_animation_status = self.animation_status

        self.image = self.sprites[self.animation_status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.start_xy_pos = tuple(self.xy_pos)
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

        self.death_zones = death_zones

    def check_fall_death(self):

        if self.rect.collidelist(self.death_zones) >= 0:
            self.xy_pos = pg.math.Vector2(self.start_xy_pos)
            self.rect.topleft = self.xy_pos

    def check_collision(self, direction):

        bottom_rect = pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 40)

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 90 pixels distance to player
            if sprite.check_distance_to_player(90):

                # contact between player and floor
                if sprite.rect.colliderect(self.rect):

                    if direction == "horizontal":
                        # left collision
                        if self.direction.x < 0:
                            if self.rect.left <= sprite.rect.right:
                                self.rect.left = sprite.rect.right
                        # right collision
                        else:
                            if self.rect.right >= sprite.rect.left:
                                self.rect.right = sprite.rect.left
                        self.xy_pos.x = self.rect.x
                    else:
                        # top collision
                        if self.rect.top <= sprite.rect.bottom:
                            self.rect.top = sprite.rect.bottom
                        # bottom collision
                        if self.rect.bottom >= sprite.rect.top:
                            self.rect.bottom = sprite.rect.top
                            contact = True
                            self.on_floor = True
                            if self.jumped:
                                self.jumped = False
                        self.xy_pos.y = self.rect.y
                        self.direction.y = 0

        # no contact between player and floor and not jumping -> falling
        if not contact and not self.jumped:
            self.on_floor = False

    def input(self):

        keys = pg.key.get_pressed()

        if len(keys) > 0:
            if self.on_floor or self.jumped:
                # horizontal input
                if keys[pg.K_RIGHT]:
                    self.direction.x = 1
                    if not self.jumped:
                        self.animation_status = "run_right"
                    else:
                        self.animation_status = "jump_right"
                elif keys[pg.K_LEFT]:
                    self.direction.x = -1
                    if not self.jumped:
                        self.animation_status = "run_left"
                    else:
                        self.animation_status = "jump_left"
                else:
                    self.direction.x = 0

            if self.on_floor and not self.jumped:
                # vertical input (jumping)
                if keys[pg.K_UP] or keys[pg.K_SPACE]:
                    self.direction.y -= self.jump_speed
                    self.on_floor = False
                    self.jumped = True

                    # initial jump animation
                    if "right" in self.animation_status:
                        self.animation_status = "jump_right"
                    else:
                        self.animation_status = "jump_left"



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

        # no movement to any direction and on floor = standing (idle) animation
        if self.direction.x == 0 and self.direction.y == 0 and self.on_floor:
            if "right" in self.animation_status:
                self.animation_status = "stand_right"
            else:
                self.animation_status = "stand_left"

    def animate(self, dt):

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if "run" in self.animation_status:
            if self.run_frame_direction > 0: # going forwards through tuple
                self.frame_index += 7 * dt
                if self.frame_index >= len(self.sprites[self.animation_status]):
                    self.frame_index = len(self.sprites[self.animation_status]) - 1
                    self.run_frame_direction = -1
            else: # going backwards through tuple
                self.frame_index -= 7 * dt
                if self.frame_index < 0:
                    self.frame_index = 0
                    self.run_frame_direction = 1
        elif "jump" in self.animation_status:
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.sprites[self.animation_status]):
                self.frame_index = len(self.sprites[self.animation_status]) - 1
        else:
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.sprites[self.animation_status]):
                self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.old_animation_status = self.animation_status
        self.input()
        self.move(dt)
        self.animate(dt)
        self.check_fall_death()
        # print(self.xy_pos)
        # print("current rect", self.rect.left)
        # print("old rect", self.old_rect.left)


