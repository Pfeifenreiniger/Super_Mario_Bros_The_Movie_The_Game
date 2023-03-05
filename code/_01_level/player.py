
import pygame as pg

from code._01_level.layers import LAYERS

class Player(pg.sprite.Sprite):
    def __init__(self, groups, pos, collision_sprites, map_width, death_zones, settings, menu_pane):
        super().__init__(groups)

        self.loaded = False

        self.settings = settings
        self.menu_pane = menu_pane

        self.sprites = {
            "stand_left" : (pg.image.load("graphics/01_excavation_site/entities/player/stand_left/player_stand_left_f1.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/stand_left/player_stand_left_f2.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/stand_left/player_stand_left_f3.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/stand_left/player_stand_left_f4.png").convert_alpha()),
            "stand_right" : (pg.image.load("graphics/01_excavation_site/entities/player/stand_right/player_stand_right_f1.png").convert_alpha(),
                             pg.image.load("graphics/01_excavation_site/entities/player/stand_right/player_stand_right_f2.png").convert_alpha(),
                             pg.image.load("graphics/01_excavation_site/entities/player/stand_right/player_stand_right_f3.png").convert_alpha(),
                             pg.image.load("graphics/01_excavation_site/entities/player/stand_right/player_stand_right_f4.png").convert_alpha(),),
            "run_left" : (pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f1.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f2.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f3.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f4.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f5.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f6.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f7.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/player/run_left/player_run_left_f8.png").convert_alpha()),
            "run_right" : (pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f1.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f2.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f3.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f4.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f5.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f6.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f7.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/run_right/player_run_right_f8.png").convert_alpha()),
            "jump_left" : (pg.image.load("graphics/01_excavation_site/entities/player/jump_left/player_jump_left_f1.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/jump_left/player_jump_left_f2.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/jump_left/player_jump_left_f3.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/jump_left/player_jump_left_f4.png").convert_alpha()),
            "jump_right" : (pg.image.load("graphics/01_excavation_site/entities/player/jump_right/player_jump_right_f1.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/jump_right/player_jump_right_f2.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/jump_right/player_jump_right_f3.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/jump_right/player_jump_right_f4.png").convert_alpha()),
            "duck_left" : (pg.image.load("graphics/01_excavation_site/entities/player/duck_left/player_duck_left_f1.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/player/duck_left/player_duck_left_f2.png").convert_alpha()),
            "duck_right" : (pg.image.load("graphics/01_excavation_site/entities/player/duck_right/player_duck_right_f1.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/player/duck_right/player_duck_right_f2.png").convert_alpha()),
            "stand_attack_right" : (pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f1.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f2.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f3.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f4.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f5.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f6.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f7.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f8.png").convert_alpha(),
                                    pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_right/player_stand_attack_right_f9.png").convert_alpha()),
            "stand_attack_left" : (pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f1.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f2.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f3.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f4.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f5.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f6.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f7.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f8.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/stand_attack_left/player_stand_attack_left_f9.png").convert_alpha()),
            "duck_attack_right" : (pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f1.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f2.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f3.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f4.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f5.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f6.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f7.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f8.png").convert_alpha(),
                                   pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_right/player_duck_attack_right_f9.png").convert_alpha()),
            "duck_attack_left" : (pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f1.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f2.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f3.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f4.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f5.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f6.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f7.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f8.png").convert_alpha(),
                                  pg.image.load("graphics/01_excavation_site/entities/player/duck_attack_left/player_duck_attack_left_f9.png").convert_alpha())
        }

        self.frame_index = 0
        self.run_frame_direction = 1
        self.animation_status = "stand_right"
        self.old_animation_status = self.animation_status

        self.image = self.sprites[self.animation_status][self.frame_index]

        self.sfx = {
            "jump" : pg.mixer.Sound("audio/sfx/player/jump.mp3"),
            "crowbar_swing" : pg.mixer.Sound("audio/sfx/player/crowbar_swing.wav"),
            "crowbar_hit" : pg.mixer.Sound("audio/sfx/player/crowbar_hit.mp3")
        }
        self.old_sfx_volume = self.settings.sfx_volume
        self.set_sfx_volume()

        self.set_hitbox(pos)
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

        self.menu_pressed = False
        self.menu_pressed_timestamp = None


    def set_sfx_volume(self):
        for sfx in self.sfx.values():
            sfx.set_volume(self.settings.sfx_volume)

    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = self.image.get_rect(topleft=pos)

        hitbox_margin = (self.rect.width / 3.2)
        hitbox_left = self.rect.left + hitbox_margin

        self.rect = pg.Rect((hitbox_left,  # left
                               self.rect.top), # top
                              (self.rect.width - (2 * hitbox_margin),  # width
                               self.rect.height)) # height

    def set_attackbox(self):
        if "stand" in self.animation_status:

            attackbox_margin_lower = self.rect.height // 2
            attackbox_margin_left = (self.rect.width // 2) if "right" in self.animation_status else 0

            self.attackbox = pg.Rect((self.rect.left + attackbox_margin_left, # left
                                      self.rect.top), # top
                                     (self.rect.width - (self.rect.width // 2), # width
                                      attackbox_margin_lower)) # height
        else:

            attachbox_margin_upper = self.rect.height // 4
            attackbox_margin_left = (self.rect.width // 2) if "right" in self.animation_status else 0

            self.attackbox = pg.Rect((self.rect.left + attackbox_margin_left, # left
                                      self.rect.top - attachbox_margin_upper), # top
                                     (self.rect.width - (self.rect.width // 2), # width
                                      attachbox_margin_upper * 3)) # height

    def check_fall_death(self):

        if self.rect.collidelist(self.death_zones) >= 0:
            self.xy_pos = pg.math.Vector2(self.start_xy_pos)
            self.rect.topleft = self.xy_pos

    def check_collision(self, direction):

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 90 pixels distance to player
            if sprite.check_distance_to_player(sprite.rect, 90):

                # contact between player rect and floor, ceiling, and walls
                if sprite.rect.colliderect(self.rect):

                    if direction == "horizontal":
                        # left collision
                        if self.direction.x < 0:
                            if self.rect.left <= sprite.rect.right:
                                self.rect.left = sprite.rect.right
                        # right collision
                        elif self.direction.x > 0:
                            if self.rect.right >= sprite.rect.left:
                                self.rect.right = sprite.rect.left
                        self.xy_pos.x = self.rect.x
                    elif direction == "vertical":
                        # top collision
                        if self.rect.top <= sprite.rect.bottom:
                            if self.direction.y < 0:
                                self.rect.top = sprite.rect.bottom
                                self.rect.top = sprite.rect.bottom
                        # bottom collision
                        if self.rect.bottom >= sprite.rect.top:
                            if self.direction.y >= 0:
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

        if not self.menu_pane.active:
            keys = pg.key.get_pressed()

            if (self.on_floor or self.jumped) and not 'attack' in self.animation_status:
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
                # vertical input
                if keys[pg.K_UP]:
                    self.direction.y -= self.jump_speed
                    self.sfx["jump"].play()
                    self.on_floor = False
                    self.jumped = True

                    # initial jump animation
                    if "right" in self.animation_status:
                        self.animation_status = "jump_right"
                    else:
                        self.animation_status = "jump_left"
                elif keys[pg.K_SPACE] and not 'attack' in self.animation_status:
                    self.sfx["crowbar_swing"].play()
                    if 'stand' in self.animation_status or 'run' in self.animation_status:
                        position = 'stand'
                    else:
                        position = 'duck'
                    self.animation_status = f"{position}_attack_{'right' if 'right' in self.animation_status else 'left'}"
                elif keys[pg.K_DOWN]:
                    if not "attack" in self.animation_status:
                        self.direction.x = 0
                        self.animation_status = f"duck_{'right' if 'right' in self.animation_status else 'left'}"
                else:
                    if self.direction.x == 0 and not 'attack' in self.animation_status:
                        self.animation_status = f"stand_{'right' if 'right' in self.animation_status else 'left'}"

                # activate menu pane
                if keys[pg.K_ESCAPE] and not self.menu_pressed:
                    self.direction.x = 0
                    self.animation_status = f"stand_{'right' if 'right' in self.animation_status else 'left'}"
                    self.menu_pane.active = True
                    self.menu_pressed = True
                    self.menu_pressed_timestamp = pg.time.get_ticks()

                if self.menu_pressed:
                    if pg.time.get_ticks() - self.menu_pressed_timestamp > 300:
                        self.menu_pressed = False


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

    def animate(self, dt):

        def return_frame_rotation_power() -> int:
            if "attack" in self.animation_status:
                return 15
            elif "duck" in self.animation_status:
                return 2
            elif "run" in self.animation_status:
                return 9
            else:
                return 7

        frame_rotation_power = return_frame_rotation_power()

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if self.direction.y > 0 and not self.jumped:  # falling -> last sprite of jumping sprites
            self.animation_status = f"jump_{'right' if 'right' in self.animation_status else 'left'}"
            self.frame_index = len(self.sprites[self.animation_status]) - 1

        elif "run" in self.animation_status:
            if self.run_frame_direction > 0: # going forwards through tuple
                self.frame_index += frame_rotation_power * dt
                if self.frame_index >= len(self.sprites[self.animation_status]):
                    self.frame_index = len(self.sprites[self.animation_status]) - 1
                    self.run_frame_direction = -1
            else: # going backwards through tuple
                self.frame_index -= frame_rotation_power * dt
                if self.frame_index < 0:
                    self.frame_index = 0
                    self.run_frame_direction = 1

        elif "jump" in self.animation_status:
            if self.direction.y < 0:
                if self.frame_index + (frame_rotation_power * dt) > len(self.sprites[self.animation_status]) - 1:
                    self.frame_index = len(self.sprites[self.animation_status]) - 2
                else:
                    self.frame_index += frame_rotation_power * dt
            else:
                self.frame_index = len(self.sprites[self.animation_status]) - 1

        elif "attack" in self.animation_status:
            self.direction.x = 0
            self.frame_index += frame_rotation_power * dt
            if int(self.frame_index) >= 2 and int(self.frame_index) <= 7:
                if not hasattr(self, 'attackbox'):
                    self.set_attackbox()

            elif int(self.frame_index) > len(self.sprites[self.animation_status]) - 1:

                if hasattr(self, 'attackbox'):
                    del self.attackbox

                if 'stand' in self.animation_status:
                    position = 'stand'
                else:
                    position = 'duck'
                self.animation_status = f"{position}_{'right' if 'right' in self.animation_status else 'left'}"
                self.frame_index = 0
                frame_rotation_power = return_frame_rotation_power()

        else:
            self.frame_index += frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites[self.animation_status]) - 1:
                self.frame_index = 0

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.old_animation_status = self.animation_status
        self.input()
        self.move(dt)
        self.animate(dt)
        self.check_fall_death()

        # print(f"RECT: {self.rect.top}")
        # print(f"HITBOX: {self.hitbox.top}")
        # print(f"XY: {self.xy_pos.y}")

        # print(self.xy_pos)
        # print("current rect", self.rect.left)
        # print("old rect", self.old_rect.left)


