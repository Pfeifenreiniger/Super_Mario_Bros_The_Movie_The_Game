
import pygame as pg
import math

class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, surf, z, player, distance_between_rects_method):
        super().__init__(groups)

        self.loaded = False

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        self.player = player

        self.check_distance_between_rects = distance_between_rects_method

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True


class CollisionTile(Tile):
    def __init__(self, groups, pos, surf, z, player, distance_between_rects_method):
        super().__init__(groups=groups,
                         pos=pos,
                         surf=surf,
                         z=z,
                         player=player,
                         distance_between_rects_method=distance_between_rects_method)

        self.hitbox = self.rect

        # self.old_rect = self.rect.copy()

class CollisionTileWithSeparateHitbox(CollisionTile):
    def __init__(self, groups, pos, surf, hitbox, z, player, distance_between_rects_method):
        super().__init__(groups=groups,
                         pos=pos,
                         surf=surf,
                         z=z,
                         player=player,
                         distance_between_rects_method=distance_between_rects_method)

        self.hitbox = hitbox # custom set hitbox
