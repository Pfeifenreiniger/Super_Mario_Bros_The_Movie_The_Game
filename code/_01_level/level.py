
import pygame as pg
import math

from pytmx.util_pygame import load_pygame
from _01_level.player import Player
from tile import Tile, CollisionTile
from layers import LAYERS


class AllSprites(pg.sprite.Group):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.screen = pg.display.get_surface()
        self.offset = pg.math.Vector2()

        # dimensions
        self.padding = self.settings.WINDOW_WIDTH // 2


    def draw_tiles(self, tile, player):
        self.offset.x = player.rect.centerx - (self.settings.WINDOW_WIDTH // 2)
        self.offset.y = player.rect.centery - (self.settings.WINDOW_HEIGHT // 2)

        offset_rect = tile.image.get_rect(center=tile.rect.center)
        offset_rect.center -= self.offset

        self.screen.blit(tile.image, offset_rect)

    def draw_player(self, sprite, player):


        self.offset.x = player.rect.centerx - (self.settings.WINDOW_WIDTH // 2)
        self.offset.y = player.rect.centery - (self.settings.WINDOW_HEIGHT // 2)

        offset_rect = sprite.image.get_rect(center=sprite.rect.center)
        offset_rect.center -= self.offset

        self.screen.blit(sprite.image, offset_rect)


class _01_Main:
    def __init__(self, event_loop, settings):
        self.event_loop = event_loop
        self.settings = settings

        # groups
        self.all_sprites = AllSprites(settings=self.settings)
        self.collision_sprites = pg.sprite.Group()

        self.setup()

    def setup(self):

        tmx_map = load_pygame("../data/01_excavation_site/01_map.tmx")

        # player
        for obj in tmx_map.get_layer_by_name('ENTITIES'):
            if obj.name == 'Player':
                self.player = Player(groups=self.all_sprites,
                                     pos=(obj.x, obj.y),
                                     collision_sprites=self.collision_sprites)

        # collision tiles
        for x, y, surf in tmx_map.get_layer_by_name('MG').tiles():
            CollisionTile(groups=[self.all_sprites, self.collision_sprites],
                 pos=(x * 20, y * 20),
                 surf=surf,
                 z=LAYERS['MG'],
                 player=self.player)

        # objects: Background
        for obj in tmx_map.get_layer_by_name('BG'):
            Tile(groups=self.all_sprites,
                 pos=(obj.x, obj.y),
                 surf=obj.image,
                 z=LAYERS['BG'],
                 player=self.player)

        # objects: Foreground
        for obj in tmx_map.get_layer_by_name('FG'):
            Tile(groups=self.all_sprites,
                 pos=(obj.x, obj.y),
                 surf=obj.image,
                 z=LAYERS['FG'],
                 player=self.player)

    def update(self, dt):

        for sprite in sorted(self.all_sprites.sprites(), key=lambda sprite: sprite.z):

            if sprite.__class__.__name__ == "Tile" or sprite.__class__.__name__ == "CollisionTile":
                if sprite.check_distance_to_player(900):
                    self.all_sprites.draw_tiles(tile=sprite,player=self.player)
            elif sprite.__class__.__name__ == "Player":
                self.player.update(dt)
                self.all_sprites.draw_player(sprite=sprite, player=self.player)



