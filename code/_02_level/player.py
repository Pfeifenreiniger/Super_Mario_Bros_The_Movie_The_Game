
import pygame as pg

from code._02_level.entity import Entity

class Player(Entity):
    def __init__(self, groups, pos, collision_sprites, map_width, map_height, settings, distance_between_rects_method):
        super().__init__(groups=groups,
                         pos=pos,
                         collision_sprites=collision_sprites,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

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

        self.image = self.sprites["stand_up"][self.frame_index]
        