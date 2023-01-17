
import pygame as pg


from pytmx.util_pygame import load_pygame
from _01_level.player import Player
from tile import Tile, CollisionTile
from layers import LAYERS


class AllSprites(pg.sprite.Group):
    def __init__(self, settings, map_width):
        super().__init__()
        self.settings = settings
        self.SCREEN = pg.display.get_surface()
        self.offset = pg.math.Vector2()

        self.map_width = map_width

    def update_offset(self, sprite, player):
        # center camera x if player is not on the map edges
        if player.rect.centerx > 400 and player.rect.centerx < self.map_width - self.settings.WINDOW_WIDTH // 2:
            self.offset.x = player.rect.centerx - self.settings.WINDOW_WIDTH // 2
        else:
            self.offset.x = 0 if player.rect.centerx <= 400 else self.map_width - self.settings.WINDOW_WIDTH
        self.offset.y = player.rect.centery - self.settings.WINDOW_HEIGHT // 2

        self.offset_rect = sprite.image.get_rect(center=sprite.rect.center)
        self.offset_rect.center -= self.offset

    def draw(self, sprite, player):

        self.update_offset(sprite, player)

        self.SCREEN.blit(sprite.image, self.offset_rect)


class _01_Main:
    def __init__(self, event_loop, settings):
        self.event_loop = event_loop
        self.settings = settings

        self.tmx_map = load_pygame("../data/01_excavation_site/01_map.tmx")
        self.map_width = self.tmx_map.tilewidth * self.tmx_map.width

        # groups
        self.all_sprites = AllSprites(settings=self.settings, map_width=self.map_width)
        self.collision_sprites = pg.sprite.Group()

        self.setup()

    def setup(self):

        # player
        for obj in self.tmx_map.get_layer_by_name('ENTITIES'):
            if obj.name == 'Player':
                self.player = Player(groups=self.all_sprites,
                                     pos=(obj.x, obj.y),
                                     collision_sprites=self.collision_sprites,
                                     map_width=self.map_width)

        # collision tiles
        for x, y, surf in self.tmx_map.get_layer_by_name('MG').tiles():
            CollisionTile(groups=[self.all_sprites, self.collision_sprites],
                 pos=(x * 20, y * 20),
                 surf=surf,
                 z=LAYERS['MG'],
                 player=self.player)

        # objects: Background
        for obj in self.tmx_map.get_layer_by_name('BG'):
            Tile(groups=self.all_sprites,
                 pos=(obj.x, obj.y),
                 surf=obj.image,
                 z=LAYERS['BG'],
                 player=self.player)

        # objects: Foreground
        for obj in self.tmx_map.get_layer_by_name('FG'):
            Tile(groups=self.all_sprites,
                 pos=(obj.x, obj.y),
                 surf=obj.image,
                 z=LAYERS['FG'],
                 player=self.player)

    def update(self, dt):

        for sprite in sorted(self.all_sprites.sprites(), key=lambda sprite: sprite.z):

            if sprite.__class__.__name__ == "Tile" or sprite.__class__.__name__ == "CollisionTile":
                if sprite.check_distance_to_player(1150):
                    self.all_sprites.draw(sprite=sprite, player=self.player)
            elif sprite.__class__.__name__ == "Player":
                self.player.update(dt)
                self.all_sprites.draw(sprite=sprite, player=self.player)



