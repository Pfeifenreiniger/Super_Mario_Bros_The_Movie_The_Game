
import pygame as pg
import math

class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, surf, z, player):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        self.player = player

    def check_distance_to_player(self, max_distance:int) -> bool:
        "max_distance in pixels"
        if math.dist(self.player.rect.midbottom, self.rect.center) < max_distance:
            return True
        else:
            return False

class CollisionTile(Tile):
    def __init__(self, groups, pos, surf, z, player):
        super().__init__(groups=groups,
                         pos=pos,
                         surf=surf,
                         z=z,
                         player=player)

        self.old_rect = self.rect.copy()


