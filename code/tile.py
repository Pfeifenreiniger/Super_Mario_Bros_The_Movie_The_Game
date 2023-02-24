
import pygame as pg
import math

class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, surf, z, player, distance_to_player_method):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        self.player = player

        self.check_distance_to_player = distance_to_player_method


class CollisionTile(Tile):
    def __init__(self, groups, pos, surf, z, player, distance_to_player_method):
        super().__init__(groups=groups,
                         pos=pos,
                         surf=surf,
                         z=z,
                         player=player,
                         distance_to_player_method=distance_to_player_method)

        # self.old_rect = self.rect.copy()


