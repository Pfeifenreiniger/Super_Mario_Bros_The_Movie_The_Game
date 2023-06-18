
import pygame as pg
import random as rnd

from pytmx.util_pygame import load_pygame
from code.check_distance_between_rects import check_distance_between_rects
from code.menu_pane import MenuPane
from code._01_level.player import Player
from code._01_level.rat import Rat
from code._01_level.bouncer import Bouncer
from code._01_level.lamp import Lamp
from code._01_level.hud import HUD
from code.tile import Tile, CollisionTile
from code._01_level.layers import LAYERS
from code.game_over import GameOverScreen
from code.cutscenes import Intro, Outro
from code.control_screen import ControlScreen


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


class _01_Main:
    def __init__(self, settings, locator):

        self.loaded = False
        self.all_sprites_loaded = False
        self.finished = False

        self.settings = settings
        self.locator = locator

        self.game_over_screen = GameOverScreen(settings)
        self.intro = Intro(1, self.settings)
        self.outro = Outro(1, self.settings)
        self.control_screen = ControlScreen(1, self.settings)

        SCREEN = self.settings.get_display_screen()
        self.menu_pane = MenuPane(screen=SCREEN, settings=self.settings, locator=locator)

        self.tmx_map = load_pygame("data/01_excavation_site/01_map.tmx")
        self.map_width = self.tmx_map.tilewidth * self.tmx_map.width
        self.map_height = self.tmx_map.tileheight * self.tmx_map.height

        # music
        self.music_volume = self.settings.music_volume
        self.music = pg.mixer.Sound("audio/music/Valmont - Old Sewers (Demake Dead Cells Soundtrack).mp3")
        self.music.set_volume(self.music_volume)
        self.music_plays = False
        # env sfx
        self.sfx_volume = self.settings.sfx_volume
        self.daisy_yells_sfx = pg.mixer.Sound("audio/sfx/environment/daisy_yells_luigi.mp3")
        self.daisy_yells_sfx.set_volume(self.sfx_volume)
        self.bg_sfx_played = False
        self.bg_sfx_timestamp = None

        # distance function
        self.check_distance_between_rects = check_distance_between_rects

        # groups
        self.all_sprites = AllSprites(screen=SCREEN, settings=self.settings, map_width=self.map_width, map_height=self.map_height)
        self.collision_sprites = pg.sprite.Group()

        self.setup()



    def setup(self):

        # objects: end zone
        for obj in self.tmx_map.get_layer_by_name('END_ZONE'):
            self.end_zone = pg.Rect(obj.x, obj.y, obj.width, obj.height)

        # objects: death zones
        death_zones = []
        for obj in self.tmx_map.get_layer_by_name('DEATH_ZONES'):
            death_zones.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
        self.death_zones = tuple(death_zones)

        # objects: ledges
        ledges = []
        for obj in self.tmx_map.get_layer_by_name('LEDGES'):
            ledges.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
        self.ledges = tuple(ledges)

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
                                menu_pane=self.menu_pane,
                                distance_between_rects_method=self.check_distance_between_rects,
                                end_zone=self.end_zone
                                )

            elif obj.name == 'Rat':
                Rat(
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    collision_sprites=self.collision_sprites,
                    map_width=self.map_width,
                    death_zones=self.death_zones,
                    ledges=self.ledges,
                    settings=self.settings,
                    player=self.player,
                    distance_between_rects_method=self.check_distance_between_rects
                )

            elif obj.name == "Bouncer1":
                Bouncer(
                    bouncer_no=1,
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    collision_sprites=self.collision_sprites,
                    map_width=self.map_width,
                    death_zones=self.death_zones,
                    ledges=self.ledges,
                    settings=self.settings,
                    player=self.player,
                    distance_between_rects_method=self.check_distance_between_rects
                )

            elif obj.name == "Bouncer2":
                Bouncer(
                    bouncer_no=2,
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    collision_sprites=self.collision_sprites,
                    map_width=self.map_width,
                    death_zones=self.death_zones,
                    ledges=self.ledges,
                    settings=self.settings,
                    player=self.player,
                    distance_between_rects_method=self.check_distance_between_rects
                )

        # tiles: collision tiles (mainground)
        for x, y, surf in self.tmx_map.get_layer_by_name('MG').tiles():
            CollisionTile(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(x * 20, y * 20),
                surf=surf,
                z=LAYERS['MG'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
                )

        # objects: mainground
        for obj in self.tmx_map.get_layer_by_name('MG_Objects'):
            if obj.name == "Lamp":
                self.lamp = Lamp(
                                groups=self.all_sprites,
                                pos=(obj.x, obj.y),
                                player=self.player,
                                distance_between_rects_method=self.check_distance_between_rects
                                )
            else:
                Tile(
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    z=LAYERS['MG_Objects'],
                    player=self.player,
                    distance_between_rects_method=self.check_distance_between_rects
                    )

        # tiles: forground
        for x, y, surf in self.tmx_map.get_layer_by_name('FG_Tiles').tiles():
            Tile(
                groups=self.all_sprites,
                pos=(x * 20, y * 20),
                surf=surf,
                z=LAYERS['FG_Tiles'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
                )

        # objects: foreground objects
        for obj in self.tmx_map.get_layer_by_name('FG_Objects'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['FG_Objects'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
                )

        # objects: background large tiles
        for obj in self.tmx_map.get_layer_by_name('BG_LargeTiles'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['BG'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
                )

        # objects: background details
        for obj in self.tmx_map.get_layer_by_name('BG_Objects'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['BG_Objects'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
                )

        # player HUD
        self.hud = HUD(
                    settings=self.settings,
                    player=self.player
                    )

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            # check loading progression of intro and outro
            self.intro.check_loading_progression()
            self.outro.check_loading_progression()
            self.control_screen.check_loading_progression()
            if self.intro.loaded and self.outro.loaded and self.control_screen.loaded:
                self.loaded = True

    def check_settings_updates(self):
        # bg music
        if self.music_volume != self.settings.music_volume:
            self.music_volume = self.settings.music_volume
            self.music.set_volume(self.music_volume)

        # bg sfx
        if self.sfx_volume != self.settings.sfx_volume:
            self.sfx_volume = self.settings.sfx_volume
            self.daisy_yells_sfx.set_volume(self.sfx_volume)

        # player sfx
        if self.player.old_sfx_volume != self.settings.sfx_volume:
            self.player.old_sfx_volume = self.settings.sfx_volume
            self.player.set_sfx_volume()

    def check_bg_sfx(self):
        if not self.bg_sfx_played:
            if rnd.randint(1,1000) > 992:
                self.daisy_yells_sfx.play()
                self.bg_sfx_timestamp = pg.time.get_ticks()
                self.bg_sfx_played = True
        else:
            if pg.time.get_ticks() - self.bg_sfx_timestamp > 5000:
                # once daisy_yells_sfx played, wait roughly 5 seconds until next sfx could be played
                self.bg_sfx_played = False
                self.bg_sfx_timestamp = None

    def check_level_finished(self):
        if self.player.check_end_zone():
            self.finished = True
            self.music.stop()

    def update_sprites(self, dt):
        for sprite in sorted(self.all_sprites.sprites(), key=lambda sprite: sprite.z):

            if sprite.__class__.__name__ == "Player":
                self.all_sprites.draw(sprite=sprite, player=self.player)
            else:
                if sprite.check_distance_between_rects(rect1=self.player.rect, rect2=sprite.rect, max_distance=1200):
                    if sprite.__class__.__name__ == "Tile" or sprite.__class__.__name__ == "CollisionTile":
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "Lamp":
                        self.lamp.update(dt)
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "Rat" or sprite.__class__.__name__ == "Bouncer":
                        sprite.update(dt)
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                else:
                    # reset enemy positions if distance between player and enemy are too far away
                    if sprite.__class__.__name__ == "Rat" or sprite.__class__.__name__ == "Bouncer":
                        sprite.xy_pos = pg.math.Vector2(sprite.start_xy_pos)

    def update(self, dt):

        if self.all_sprites_loaded:

            if not self.finished:

                if self.intro.done and not self.music_plays:
                    # music plays as soon as the intro is done
                    self.music.play(loops=-1)
                    self.music_plays = True

                if not self.player.dead:
                    self.player.update(dt)

                    self.check_level_finished()

                    self.update_sprites(dt)

                    self.check_bg_sfx()

                    # pause menu in front if active (and level not finished)
                    if self.menu_pane.active and not self.finished:
                        self.menu_pane.update(dt)
                        self.menu_pane.draw()

                        self.check_settings_updates()

                    # else player hud in front
                    else:
                        self.hud.draw()

                    if self.locator.current_location != 1:
                        self.music.stop()
                else:
                    self.music.stop()
                    if self.game_over_screen.restart_game:
                        self.game_over_screen.music.stop()
                        del self.game_over_screen
                        self.locator.current_location = 0
                    elif self.game_over_screen.restart_level:
                        self.game_over_screen.music.stop()
                        self.__init__(settings=self.settings,locator=self.locator)
                    else:
                        self.game_over_screen.update()
                        self.game_over_screen.draw()

        else:
            while not self.all_sprites_loaded:
                all_true = True
                for sprite in self.all_sprites:
                    sprite.check_loading_progression()
                    if not sprite.loaded:
                        all_true = False
                        break
                if all_true:
                    self.all_sprites_loaded = True
