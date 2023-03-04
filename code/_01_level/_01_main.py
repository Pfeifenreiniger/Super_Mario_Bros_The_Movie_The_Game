
import pygame as pg
import math

from pytmx.util_pygame import load_pygame
from menu_pane import MenuPane
from _01_level.player import Player
from _01_level.lamp import Lamp
from tile import Tile, CollisionTile
from layers import LAYERS


class AllSprites(pg.sprite.Group):
    def __init__(self, settings, map_width, map_height):
        super().__init__()
        self.settings = settings
        self.SCREEN = pg.display.get_surface()
        self.offset = pg.math.Vector2()

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


class _01_Main:
    def __init__(self, event_loop, settings, locator):

        self.loaded = False

        self.event_loop = event_loop
        self.settings = settings
        self.locator = locator

        SCREEN = self.settings.get_display_screen()
        self.menu_pane = MenuPane(screen=SCREEN, settings=self.settings, locator=locator)

        self.tmx_map = load_pygame("../data/01_excavation_site/01_map.tmx")
        self.map_width = self.tmx_map.tilewidth * self.tmx_map.width
        self.map_height = self.tmx_map.tileheight * self.tmx_map.height

        # music
        self.music_volume = self.settings.music_volume
        self.music = pg.mixer.Sound("../audio/music/Valmont - Old Sewers (Demake Dead Cells Soundtrack).mp3")
        self.music.set_volume(self.music_volume)
        self.music.play(loops=-1)

        # groups
        self.all_sprites = AllSprites(settings=self.settings, map_width=self.map_width, map_height=self.map_height)
        self.collision_sprites = pg.sprite.Group()

        self.setup()



    def setup(self):

        # objects: death zones
        death_zones = []
        for obj in self.tmx_map.get_layer_by_name('DEATH_ZONES'):
            death_zones.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
        self.death_zones = tuple(death_zones)

        # entities
        for obj in self.tmx_map.get_layer_by_name('ENTITIES'):
            if obj.name == 'Player':
                self.player = Player(
                                groups=self.all_sprites,
                                pos=(obj.x, obj.y),
                                collision_sprites=self.collision_sprites,
                                map_width=self.map_width,
                                death_zones=self.death_zones,
                                settings=self.settings,
                                menu_pane=self.menu_pane
                                )

        # tiles: collision tiles (mainground)
        for x, y, surf in self.tmx_map.get_layer_by_name('MG').tiles():
            CollisionTile(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(x * 20, y * 20),
                surf=surf,
                z=LAYERS['MG'],
                player=self.player,
                distance_to_player_method=self.check_distance_to_player
                )

        # objects: mainground
        for obj in self.tmx_map.get_layer_by_name('MG_Objects'):
            if obj.name == "Lamp":
                self.lamp = Lamp(
                                groups=self.all_sprites,
                                pos=(obj.x, obj.y),
                                player=self.player,
                                distance_to_player_method=self.check_distance_to_player
                                )
            else:
                Tile(
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    z=LAYERS['MG_Objects'],
                    player=self.player,
                    distance_to_player_method=self.check_distance_to_player
                    )

        # tiles: forground
        for x, y, surf in self.tmx_map.get_layer_by_name('FG_Tiles').tiles():
            Tile(
                groups=self.all_sprites,
                pos=(x * 20, y * 20),
                surf=surf,
                z=LAYERS['FG_Tiles'],
                player=self.player,
                distance_to_player_method=self.check_distance_to_player
                )

        # objects: foreground objects
        for obj in self.tmx_map.get_layer_by_name('FG_Objects'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['FG_Objects'],
                player=self.player,
                distance_to_player_method=self.check_distance_to_player
                )

        # objects: background large tiles
        for obj in self.tmx_map.get_layer_by_name('BG_LargeTiles'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['BG'],
                player=self.player,
                distance_to_player_method=self.check_distance_to_player
                )

        # objects: background details
        for obj in self.tmx_map.get_layer_by_name('BG_Objects'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['BG_Objects'],
                player=self.player,
                distance_to_player_method=self.check_distance_to_player
                )

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True

    def check_distance_to_player(self, rect:pg.Rect, max_distance:int) -> bool:
        """Method to pass to any graphical objects except the player.
        It will calculate the distance between said objects and the player's current position in pixels.
        The object's rectangle has to be passed to the parameter 'rect='.
        If the distance between the player's rectangle center position and those of the passed object's rectangle
        center position exceeds the set maximum (parameter 'max_distance=') a boolean false will be returned,
        otherwise true."""

        if math.dist(self.player.rect.center, rect.center) < max_distance:
            return True
        else:
            return False

    def check_settings_updates(self):
        # bg music
        if self.music_volume != self.settings.music_volume:
            self.music_volume = self.settings.music_volume
            self.music.set_volume(self.music_volume)

        # player sfx
        if self.player.old_sfx_volume != self.settings.sfx_volume:
            self.player.old_sfx_volume = self.settings.sfx_volume
            self.player.set_sfx_volume()

    def update_sprites(self, dt):
        for sprite in sorted(self.all_sprites.sprites(), key=lambda sprite: sprite.z):

            if sprite.__class__.__name__ == "Player":
                self.all_sprites.draw(sprite=sprite, player=self.player)
            else:
                if sprite.check_distance_to_player(sprite.rect, 1200):
                    if sprite.__class__.__name__ == "Tile" or sprite.__class__.__name__ == "CollisionTile":
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "Lamp":
                        self.lamp.update(dt)
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "Player":
                        self.all_sprites.draw(sprite=sprite, player=self.player)

    def update(self, dt):

        if self.player.loaded:

            self.player.update(dt)

            self.update_sprites(dt)

            # pause menu in front if active
            if self.menu_pane.active:
                self.menu_pane.update(dt)
                self.menu_pane.draw()

                self.check_settings_updates()

            if self.locator.current_location != 1:
                self.music.stop()

        else:
            self.player.check_loading_progression()

