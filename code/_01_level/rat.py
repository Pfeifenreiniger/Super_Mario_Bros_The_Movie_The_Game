import pygame as pg

from code._01_level.entity import Entity

class Rat(Entity):
    def __init__(self, groups, pos, collision_sprites, map_width, death_zones, settings, player, distance_between_rects_method):
        super().__init__(groups, pos, collision_sprites, death_zones, settings, map_width, distance_between_rects_method)

        self.player = player

        self.sprites = {
            "stand_left" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_left/rat_stand_left_f1.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_left/rat_stand_left_f2.png").convert_alpha()),
            "stand_right" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_right/rat_stand_right_f1.png").convert_alpha(),
                             pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_right/rat_stand_right_f2.png").convert_alpha())
        }

        self.image = self.sprites[self.animation_status][self.frame_index]
        self.set_hitbox(pos)
        self.xy_pos = pg.math.Vector2(self.rect.topleft)
        self.start_xy_pos = tuple(self.xy_pos)


    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = self.image.get_rect(topleft=pos)

        hitbox_margin = (self.rect.width // 2)
        if "right" in self.animation_status:
            hitbox_left = self.rect.left + hitbox_margin
        else:
            hitbox_left = self.rect.left

        if "left" in self.animation_status:
            hitbox_right = self.rect.right - hitbox_margin
        else:
            hitbox_right = self.rect.right

        self.rect = pg.Rect((hitbox_left,  # left
                               self.rect.top), # top
                              (self.rect.width - hitbox_margin,  # width
                               self.rect.height)) # height

    def check_collision(self, direction):

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 90 pixels distance to player
            if sprite.check_distance_between_rects(rect1=self.rect, rect2=sprite.rect, max_distance=90):

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
                        self.xy_pos.y = self.rect.y
                        self.direction.y = 0

        # no contact between rat and floor -> falling
        if not contact:
            self.on_floor = False

    def face_player(self):
        if self.rect.centerx < self.player.rect.centerx:
            if "stand" in self.animation_status:
                self.animation_status = "stand_right"
        else:
            if "stand" in self.animation_status:
                self.animation_status = "stand_left"

    def animate(self, dt):

        def return_frame_rotation_power() -> int:
            if "attack" in self.animation_status:
                return 15
            else:
                return 3

        frame_rotation_power = return_frame_rotation_power()

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if "stand" in self.animation_status:
            self.frame_index += frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites[self.animation_status]):
                self.frame_index = 0

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]

    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.move(dt)
        self.face_player()
        self.animate(dt)
        self.check_fall_death()

