
import pygame as pg

from pytmx.util_pygame import load_pygame
from code.game_over import GameOverScreen
from code.tile import Tile, CollisionTile

class AllSprites(pg.sprite.Group):
    def __init__(self, screen, settings, map_width, map_height):
        super().__init__()
        self.offset = pg.math.Vector2()
        self.SCREEN = screen
        self.settings = settings
        self.map_width = map_width
        self.map_height = map_height

    def update_offset(self, sprite, player):
        # center camera x if player is not on the map outer edges
        if player.rect.centerx > 400 and player.rect.centerx < self.map_width - self.settings.WINDOW_WIDTH // 2:
            self.offset.x = player.rect.centerx - self.settings.WINDOW_WIDTH // 2

            # positive parallax scrolling for foreground tiles
            if sprite.z == LAYERS['FG_Tiles'] or sprite.z == LAYERS['FG_Objects']:
                self.offset.x = self.offset.x * 1.2

        else:
            self.offset.x = 0 if player.rect.centerx <= 400 else self.map_width - self.settings.WINDOW_WIDTH

        # center camera y of player is not on the map lower edge
        if player.rect.centery < self.map_height - self.settings.WINDOW_HEIGHT // 2:
            self.offset.y = player.rect.centery - self.settings.WINDOW_HEIGHT // 1.8
        else:
            self.offset.y = self.map_height - self.settings.WINDOW_HEIGHT

        self.offset_rect = sprite.image.get_rect(center=sprite.rect.center)
        self.offset_rect.center -= self.offset

    def draw(self, sprite, player):

        self.update_offset(sprite, player)

        self.SCREEN.blit(sprite.image, self.offset_rect)


class _02_Main:
    def __init__(self, event_loop, settings, locator):

        self.loaded = False
        self.all_sprites_loaded = False
        self.finished = False

        self.event_loop = event_loop
        self.settings = settings
        self.locator = locator

        self.game_over_screen = GameOverScreen(settings)

        SCREEN = self.settings.get_display_screen()

        self.tmx_map = load_pygame("data/02_streets_of_dinohattan/02_map.tmx")
        self.map_width = self.tmx_map.tilewidth * self.tmx_map.width
        self.map_height = self.tmx_map.tileheight * self.tmx_map.height
        print(f"{self.map_width}x{self.map_height}")

        # groups
        self.all_sprites = AllSprites(screen=SCREEN, settings=self.settings, map_width=self.map_width, map_height=self.map_height)
        self.collision_sprites = pg.sprite.Group()

    def setup(self):
        for x, y, surf in self.tmx_map.get_layer_by_name('background').tiles():
            Tile(
                groups=self.all_sprites,
                pos=(x * 400, y * 390),
                surf=surf,
                z=LAYERS['BG'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )