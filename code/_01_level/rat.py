import pygame as pg

from code._01_level.enemy import Enemy

class Rat(Enemy):
    def __init__(self, groups, pos, collision_sprites, map_width, death_zones, ledges, settings, player, distance_between_rects_method):

        self.sprites = {
            "stand_left" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_left/rat_stand_left_f1.png").convert_alpha(),
                            pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_left/rat_stand_left_f2.png").convert_alpha()),
            "stand_right" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_right/rat_stand_right_f1.png").convert_alpha(),
                             pg.image.load("graphics/01_excavation_site/entities/enemies/rat/stand_right/rat_stand_right_f2.png").convert_alpha()),
            "run_left" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f1.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f2.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f3.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f4.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f5.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f6.png").convert_alpha(),
                          pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_left/rat_run_left_f7.png").convert_alpha()),
            "run_right" : (pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f1.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f2.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f3.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f4.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f5.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f6.png").convert_alpha(),
                           pg.image.load("graphics/01_excavation_site/entities/enemies/rat/run_right/rat_run_right_f7.png").convert_alpha())
        }

        self.image = self.sprites["stand_left"][0]

        super().__init__(groups, pos, collision_sprites, death_zones, ledges, settings, map_width, player, distance_between_rects_method)

        self.set_sfx_volume()

        self.health = 30
        self.speed = 150

        self.knockback = 10


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


    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.face_player()
        self.run_to_player()
        self.move(dt)
        self.animate(dt)
        self.deal_damage()
        self.get_damage(self.knockback)
        self.check_fall_death()

