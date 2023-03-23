import pygame as pg

from code._01_level.enemy import Enemy

class Bouncer(Enemy):
    def __init__(self, bouncer_no, groups, pos, collision_sprites, map_width, death_zones, ledges, settings, player, distance_between_rects_method):

        self.bouncer_no = bouncer_no

        self.sprites = {
            "stand_left" : (pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_left/bouncer{self.bouncer_no}_stand_left_f1.png").convert_alpha(),
                            pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_left/bouncer{self.bouncer_no}_stand_left_f2.png").convert_alpha(),
                            pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_left/bouncer{self.bouncer_no}_stand_left_f3.png").convert_alpha(),
                            pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_left/bouncer{self.bouncer_no}_stand_left_f4.png").convert_alpha()),
            "stand_right" : (pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_right/bouncer{self.bouncer_no}_stand_right_f1.png").convert_alpha(),
                             pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_right/bouncer{self.bouncer_no}_stand_right_f2.png").convert_alpha(),
                             pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_right/bouncer{self.bouncer_no}_stand_right_f3.png").convert_alpha(),
                             pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/stand_right/bouncer{self.bouncer_no}_stand_right_f4.png").convert_alpha()),
            "run_left" : (pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f1.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f2.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f3.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f4.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f5.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f6.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f7.png").convert_alpha(),
                          pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_left/bouncer{self.bouncer_no}_run_left_f8.png").convert_alpha()),
            "run_right" : (pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f1.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f2.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f3.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f4.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f5.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f6.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f7.png").convert_alpha(),
                           pg.image.load(f"graphics/01_excavation_site/entities/enemies/bouncer/{self.bouncer_no}/run_right/bouncer{self.bouncer_no}_run_right_f8.png").convert_alpha())
        }

        self.image = self.sprites["stand_left"][0]

        super().__init__(groups, pos, collision_sprites, death_zones, ledges, settings, map_width, player, distance_between_rects_method)

        self.set_sfx_volume()

        self.health = 80 if self.bouncer_no == 1 else 60
        self.speed = 110 if self.bouncer_no == 1 else 130

        self.knockback = 4 if self.bouncer_no == 1 else 6


    def set_hitbox(self, pos):
        """generates rect object and adjust its size to be the hitbox"""

        self.rect = self.image.get_rect(topleft=pos)

        hitbox_margin = (self.rect.width / 4)
        hitbox_left = self.rect.left + hitbox_margin

        self.rect = pg.Rect((hitbox_left,  # left
                             self.rect.top),  # top
                            (self.rect.width - (2 * hitbox_margin),  # width
                             self.rect.height))  # height


    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.face_player()
        self.run_to_player()
        self.move(dt)
        self.animate(dt)
        self.deal_damage()
        self.get_damage(self.knockback)
        self.check_fall_death()

