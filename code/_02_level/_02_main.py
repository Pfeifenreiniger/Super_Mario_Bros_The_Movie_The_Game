
import pygame as pg

from code._02_level.layers import LAYERS
from pytmx.util_pygame import load_pygame
from code.check_distance_between_rects import check_distance_between_rects
from code.menu_pane import MenuPane
from code.game_over import GameOverScreen
from code.tile import Tile, CollisionTile, CollisionTileWithSeparateHitbox

from code._02_level.traffic_light import TrafficLight
from code._02_level.player import Player
from code._02_level.car import CarsTimer
from code._02_level.pedestrian import PedestriansTimer
from code._02_level.train import Train
from code._02_level.bertha import Bertha
from code._02_level.hud import HUD
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
        # center camera x if player is not on the map outer horizontal edges
        if player.rect.centerx > 400 and player.rect.centerx < self.map_width - self.settings.WINDOW_WIDTH // 2:
            self.offset.x = player.rect.centerx - self.settings.WINDOW_WIDTH // 2

        else:
            self.offset.x = 0 if player.rect.centerx <= 400 else self.map_width - self.settings.WINDOW_WIDTH

        # center camera y of player is not on the map outer vertical edges
        if player.rect.centery > 300 and player.rect.centery < self.map_height - self.settings.WINDOW_HEIGHT // 2:
            self.offset.y = player.rect.centery - self.settings.WINDOW_HEIGHT // 2

            # positive parallax scrolling for train rail track and train
            if sprite.z == LAYERS['FG3'] or sprite.z == LAYERS['FG4']:
                self.offset.y = self.offset.y * 1.4

        else:
            self.offset.y = 0 if player.rect.centery <= 300 else self.map_height - self.settings.WINDOW_HEIGHT

        self.offset_rect = sprite.image.get_rect(center=sprite.rect.center)
        self.offset_rect.center -= self.offset

    def draw(self, sprite, player):

        self.update_offset(sprite, player)

        self.SCREEN.blit(sprite.image, self.offset_rect)


class _02_Main:
    def __init__(self, event_loop, settings, locator, savegames):

        self.loaded = False
        self.all_sprites_loaded = False
        self.finished = False

        self.event_loop = event_loop
        self.settings = settings
        self.locator = locator
        savegames.update_level(2)

        self.game_over_screen = GameOverScreen(settings)
        self.intro = Intro(2, self.settings)
        self.outro = Outro(2, self.settings)
        self.control_screen = ControlScreen(2, self.settings)

        SCREEN = self.settings.get_display_screen()
        self.menu_pane = MenuPane(screen=SCREEN, settings=self.settings, locator=locator, savegames=savegames)

        self.tmx_map = load_pygame("data/02_streets_of_dinohattan/02_map.tmx")
        self.map_width = self.tmx_map.tilewidth * self.tmx_map.width
        self.map_height = self.tmx_map.tileheight * self.tmx_map.height

        # music
        self.music_volume = self.settings.music_volume
        self.music = pg.mixer.Sound("audio/music/Aim To Head - Heroez.mp3")
        self.music.set_volume(self.music_volume)
        self.music_plays = False

        # distance function
        self.check_distance_between_rects = check_distance_between_rects

        # groups
        self.all_sprites = AllSprites(screen=SCREEN, settings=self.settings, map_width=self.map_width, map_height=self.map_height)
        self.collision_sprites = pg.sprite.Group()
        self.cars_sprites = pg.sprite.Group()
        self.pedestrians_sprites = pg.sprite.Group()

        # timers lists
        self.cars_timers = []
        self.pedestrians_timers = []

        self.setup()

    def setup(self):

        def calc_hitbox(surf:pg.Surface,
                        pos:tuple(),
                        margin_left:int,
                        margin_top:int,
                        margin_right:int,
                        margin_bottom:int) -> pg.Rect:

            rect = surf.get_rect(topleft=pos)

            hitbox_left = rect.left + margin_left
            hitbox_top = rect.top + margin_top

            hitbox_width = rect.width - (margin_left + margin_right)
            hitbox_height = rect.height - (margin_top + margin_bottom)

            return pg.Rect(
                (hitbox_left,
                 hitbox_top),
                (hitbox_width,
                 hitbox_height)
            )

        # end zone
        for obj in self.tmx_map.get_layer_by_name('end_zone'):
            end_zone = pg.Rect(obj.x, obj.y, obj.width, obj.height)

        # entities - player
        for obj in self.tmx_map.get_layer_by_name('entities'):
            if obj.name == 'player':
                self.player = Player(
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    collision_sprites=self.collision_sprites,
                    map_width=self.map_width,
                    map_height=self.map_height,
                    settings=self.settings,
                    menu_pane=self.menu_pane,
                    distance_between_rects_method=self.check_distance_between_rects,
                    end_zone=end_zone
                )

        # entities - bertha
            elif obj.name == 'bertha':
                Bertha(
                    groups=self.all_sprites,
                    pos=(obj.x, obj.y),
                    collision_sprites=self.collision_sprites,
                    map_width=self.map_width,
                    map_height=self.map_height,
                    settings=self.settings,
                    distance_between_rects_method=self.check_distance_between_rects
                )

        # traffic light
        for obj in self.tmx_map.get_layer_by_name('traffic_light'):
            self.traffic_light = TrafficLight(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # entities - cars
        for obj in self.tmx_map.get_layer_by_name('entities'):
            if 'cars' in obj.name:
                self.cars_timers.append(
                    CarsTimer(
                        groups=[self.all_sprites, self.cars_sprites],
                        cars_start_pos_no=int(obj.name.split('_')[1]),
                        pos=(obj.x, obj.y),
                        player=self.player,
                        distance_between_rects_method=self.check_distance_between_rects,
                        event_loop=self.event_loop,
                        settings=self.settings,
                        map_width=self.map_width,
                        map_height=self.map_height,
                        traffic_light=self.traffic_light
                    )
                )

        # entities - pedestrians
        for obj in self.tmx_map.get_layer_by_name('entities'):
            if 'pedestrians' in obj.name:
                self.pedestrians_timers.append(
                    PedestriansTimer(
                        groups=[self.all_sprites, self.pedestrians_sprites],
                        pedestrians_start_pos_no=int(obj.name.split('_')[1]),
                        pos=(obj.x, obj.y),
                        player=self.player,
                        distance_between_rects_method=self.check_distance_between_rects,
                        event_loop=self.event_loop,
                        settings=self.settings,
                        map_width=self.map_width,
                        map_height=self.map_height
                    )
                )

        # train
        for obj in self.tmx_map.get_layer_by_name('train'):
            Train(
                groups=self.all_sprites,
                surf=obj.image,
                pos=(obj.x, obj.y + 8),
                map_width=self.map_width,
                map_height=self.map_height,
                settings=self.settings,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # background
        for x, y, surf in self.tmx_map.get_layer_by_name('background').tiles():
            Tile(
                groups=self.all_sprites,
                pos=(x * 400, y * 390),
                surf=surf,
                z=LAYERS['BG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # garbage containers
        for obj in self.tmx_map.get_layer_by_name('garbage_containers'):
            CollisionTile(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # phone box
        for obj in self.tmx_map.get_layer_by_name('phone_box'):
            CollisionTileWithSeparateHitbox(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                hitbox=calc_hitbox(obj.image, (obj.x, obj.y), 4, 3, 124, 100),
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # hydrant
        for obj in self.tmx_map.get_layer_by_name('hydrant'):
            CollisionTileWithSeparateHitbox(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                hitbox=calc_hitbox(obj.image, (obj.x, obj.y), 2, 2, 2, 36),
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # street lights - single
        for obj in self.tmx_map.get_layer_by_name('street_lights_single'):
            CollisionTileWithSeparateHitbox(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                hitbox=calc_hitbox(obj.image, (obj.x, obj.y), 77, 102, 77, 117),
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # street lights - double
        for obj in self.tmx_map.get_layer_by_name('street_lights_double'):
            CollisionTileWithSeparateHitbox(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                hitbox=calc_hitbox(obj.image, (obj.x, obj.y), 110, 161, 110, 161),
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # buildings shadows
        for obj in self.tmx_map.get_layer_by_name('buildings_shadows'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['FG1'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # buildings
        for obj in self.tmx_map.get_layer_by_name('buildings'):

            margin_left:int
            margin_top:int
            margin_right:int
            margin_bottom:int

            if obj.name == '1' or obj.name == 4:
                margin_left = 8
                margin_top = 62
                margin_right = 42
                margin_bottom = 32
            elif obj.name == '2' or obj.name == '3':
                margin_left = 42
                margin_top = 62
                margin_right = 8
                margin_bottom = 32
            elif obj.name == '5' or obj.name == '7':
                margin_left = 42
                margin_top = 32
                margin_right = 8
                margin_bottom = 62
            elif obj.name == '6' or obj.name == '8':
                margin_left = 8
                margin_top = 32
                margin_right = 42
                if obj.name == '6':
                    margin_bottom = 62
                else:
                    margin_bottom = 120

            CollisionTileWithSeparateHitbox(
                groups=[self.all_sprites, self.collision_sprites],
                pos=(obj.x, obj.y),
                surf=obj.image,
                hitbox=calc_hitbox(obj.image, (obj.x, obj.y), margin_left, margin_top, margin_right, margin_bottom),
                z=LAYERS['FG2'],
                player=self.player,
                distance_between_rects_method=self.check_distance_between_rects
            )

        # train rail track
        for obj in self.tmx_map.get_layer_by_name('rail_track'):
            Tile(
                groups=self.all_sprites,
                pos=(obj.x, obj.y),
                surf=obj.image,
                z=LAYERS['FG3'],
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
            self.loaded = True

    def check_level_finished(self):
        if self.player.check_end_zone():
            self.finished = True
            self.music.stop()

    def update_cars_timers(self):
        for cars_timer in self.cars_timers:
            cars_timer.update()

    def update_pedestrians_timers(self):
        for pedestrians_timer in self.pedestrians_timers:
            pedestrians_timer.update()

    def update_sprites(self, dt):
        for sprite in sorted(self.all_sprites.sprites(), key=lambda sprite: sprite.z):

            if sprite.__class__.__name__ == "Player":
                self.all_sprites.draw(sprite=sprite, player=self.player)
            elif sprite.__class__.__name__ == "Car":
                if sprite.check_distance_between_rects(rect1=self.player.rect, rect2=sprite.rect, max_distance=3400):
                    sprite.update(dt)
                    self.all_sprites.draw(sprite=sprite, player=self.player)
                else:
                    sprite.kill()
            elif sprite.__class__.__name__ == "Pedestrian":
                if sprite.check_distance_between_rects(rect1=self.player.rect, rect2=sprite.rect, max_distance=3400):
                    sprite.update(dt)
                    self.all_sprites.draw(sprite=sprite, player=self.player)
                else:
                    sprite.kill()
            elif sprite.__class__.__name__ == "Train":
                sprite.update(dt)
                self.all_sprites.draw(sprite=sprite, player=self.player)
            else:
                if sprite.check_distance_between_rects(rect1=self.player.rect, rect2=sprite.rect, max_distance=1200):
                    if sprite.__class__.__name__ == "Tile" or sprite.__class__.__name__ == "CollisionTile" or sprite.__class__.__name__ == "CollisionTileWithSeparateHitbox":
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "TrafficLight":
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "StartArrow":
                        if not sprite.is_init:
                            sprite.is_init = True
                            sprite.init_timestamps()
                        sprite.update()
                        if sprite.is_visible:
                            self.all_sprites.draw(sprite=sprite, player=self.player)
                    elif sprite.__class__.__name__ == "Bertha":
                        if not sprite.is_init:
                            sprite.is_init = True
                        sprite.update(dt)
                        self.all_sprites.draw(sprite=sprite, player=self.player)
                    else:
                        self.all_sprites.draw(sprite=sprite, player=self.player)

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
                    self.traffic_light.update()
                    self.update_cars_timers()
                    self.update_pedestrians_timers()
                    self.update_sprites(dt)

                    if self.music_volume != self.settings.music_volume:
                        self.music_volume = self.settings.music_volume
                        self.music.set_volume(self.music_volume)

                    if self.menu_pane.active and not self.finished:
                        self.menu_pane.update(dt)
                        self.menu_pane.draw()
                    else:
                        self.hud.draw()

                    if self.locator.current_location != 2:
                        self.music.stop()

                else:
                    self.music.stop()
                    if self.game_over_screen.restart_game:
                        self.game_over_screen.music.stop()
                        del self.game_over_screen
                        self.locator.current_location = 0
                    elif self.game_over_screen.restart_level:
                        self.game_over_screen.music.stop()
                        self.__init__(settings=self.settings, locator=self.locator, event_loop=self.event_loop)
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
