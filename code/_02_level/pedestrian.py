
import pygame as pg
import random as rnd

from code._02_level.base_loading import BaseLoading
from code._02_level.layers import LAYERS
from code._02_level.entity import Entity

class Pedestrian(Entity):
    def __init__(self,
                 groups,
                 pos,
                 pedestrian_line,
                 pedestrian_no,
                 player,
                 settings,
                 map_width,
                 map_height,
                 distance_between_rects_method):

        pos = self.randomize_y_pos(pos)

        # pedestrian 5 has only 4 frames, the others 6
        sprites = []
        numb_of_frames = 6 if not pedestrian_no == 5 else 4
        for i in range(numb_of_frames):
            sprites.append(
                pg.image.load(f"graphics/02_streets_of_dinohattan/entities/pedestrians/pedestrian_{pedestrian_no}/pedestrian_{pedestrian_no}_walk_right_f{i+1}.png").convert_alpha()
            )

        self.sprites = sprites
        self.frame_index = 0
        self.image = self.sprites[self.frame_index]
        self.frame_rotation_power = 6
        self.walk_frame_direction = 1

        self.pedestrian_no = pedestrian_no
        self.pedestrian_line = pedestrian_line

        super().__init__(groups=groups,
                         pos=pos,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.pedestrians_sprites = groups[1]
        self.set_hitbox(pos)
        self.set_direction()
        self.sprites = tuple(self.sprites)

        self.speed = 100

        self.player = player

        self.shadow = PedestrianShadow(
            groups=groups[0],
            pedestrian_direction=self.direction,
            pedestrian_no=pedestrian_no,
            x_pos=self.xy_pos.x,
            y_pos=self.xy_pos.y,
            distance_between_rects_method=distance_between_rects_method
        )

        # sfx
        self.sfx_volume = self.settings.music_volume
        self.yelling_sfx = pg.mixer.Sound(f"audio/sfx/enemies/pedestrians/pedestrian{pedestrian_no}_yelling.mp3")
        self.yelling_sfx.set_volume(self.sfx_volume)
        self.yelling_sfx_played = False
        self.yelling_sfx_timestamp = None

    def randomize_y_pos(self, pos:tuple[int, int]) -> tuple[int, int]:
        return (pos[0], pos[1] + rnd.randint(-2, 2))

    def set_hitbox(self, pos):
        self.rect = self.image.get_rect(center = pos)

        if self.pedestrian_no == 1 or self.pedestrian_no == 2:
            margin_left = self.rect.width // 5
        elif self.pedestrian_no == 5:
            margin_left = self.rect.width // 8
        else:
            margin_left = self.rect.width // 4
        margin_top = self.rect.height // 8

        hitbox_left = self.rect.left + margin_left
        hitbox_top = self.rect.top + margin_top

        self.hitbox = pg.Rect(
                            (hitbox_left, # left
                             hitbox_top), # top
                            (self.rect.width - (2 * margin_left), # width
                             self.rect.height - (2 * margin_top)) # height
                            )

    def set_direction(self):
        if self.xy_pos.x < 600: # moving to the right
            self.direction.x = 1

        else: # moving to the left
            self.direction.x = -1
            sprites = []
            for image in self.sprites:
                image = pg.transform.flip(image, True, False)
                sprites.append(image)
            self.sprites = sprites

    def check_player_collision(self):
        if self.hitbox.colliderect(self.player.rect):
            self.player.get_pushed(pusher_hitbox=self.hitbox)
            if self.yelling_sfx_timestamp is None:
                self.yelling_sfx_timestamp = pg.time.get_ticks()
                self.yelling_sfx.play()
            else:
                if pg.time.get_ticks() - self.yelling_sfx_timestamp > 1000:
                    self.yelling_sfx_timestamp = pg.time.get_ticks()
                    self.yelling_sfx.play()

    def animate(self, dt):

        if self.walk_frame_direction > 0: # going forward through tuple
            self.frame_index += self.frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites):
                self.frame_index = len(self.sprites) - 1
                self.walk_frame_direction = -1
        else: # going backwards through tuple
            self.frame_index -= self.frame_rotation_power * dt
            if int(self.frame_index) < 0:
                self.frame_index = 0
                self.walk_frame_direction = 1

        self.image = self.sprites[int(self.frame_index)]

    def update_shadow(self):

        self.shadow.update_xy_pos(x=self.xy_pos.x, y=self.xy_pos.y)

    def check_sfx_vol(self):
        if self.sfx_volume != self.settings.sfx_volume:
            self.sfx_volume = self.settings.sfx_volume
            self.yelling_sfx.set_volume(self.sfx_volume)

    def update(self, dt):
        self.move(dt)
        self.update_shadow()
        self.animate(dt)
        self.hitbox = self.rect

        self.check_player_collision()

        self.check_sfx_vol()

        if not -100 < self.rect.x < 3300:
            self.shadow.kill()
            self.kill()


class PedestrianShadow(pg.sprite.Sprite, BaseLoading):
    def __init__(self, groups, pedestrian_direction:pg.Vector2, pedestrian_no:int, x_pos:int, y_pos:int, distance_between_rects_method):

        pg.sprite.Sprite.__init__(self, groups)
        BaseLoading.__init__(self)

        self.sprites = {
            '32x32': pg.image.load("graphics/02_streets_of_dinohattan/entities/pedestrians/shadows/pedestrian_shadow_32x32px.png").convert_alpha(),
            '34x34' : pg.image.load("graphics/02_streets_of_dinohattan/entities/pedestrians/shadows/pedestrian_shadow_34x34px.png").convert_alpha(),
            '36x36': pg.image.load("graphics/02_streets_of_dinohattan/entities/pedestrians/shadows/pedestrian_shadow_36x36px.png").convert_alpha(),
            '50x32': pg.image.load("graphics/02_streets_of_dinohattan/entities/pedestrians/shadows/pedestrian_shadow_50x32px.png").convert_alpha()
        }

        self.image = self.load_image(pedestrian_no)

        self.xy_pos = pg.math.Vector2(x_pos, y_pos)
        self.y_pos_margin = 5
        self.x_pos_margin = 4 if pedestrian_direction.x > 0 else 2

        self.rect = self.image.get_rect(topleft=self.xy_pos)

        self.z = LAYERS['BG2']

        self.check_distance_between_rects = distance_between_rects_method

    def load_image(self, pedestrian_no):

        match pedestrian_no:
            case 1: return self.sprites['36x36']
            case 2: return self.sprites['34x34']
            case 3: return self.sprites['34x34']
            case 4: return self.sprites['34x34']
            case 5: return self.sprites['50x32']
            case 6: return self.sprites['36x36']
            case 7: return self.sprites['34x34']
            case 8: return self.sprites['36x36']
            case 9: return self.sprites['36x36']
            case 10: return self.sprites['32x32']

    def update_xy_pos(self, x, y):

        self.xy_pos.x = x + self.x_pos_margin
        self.xy_pos.y = y + self.y_pos_margin
        self.rect.x = round(self.xy_pos.x)
        self.rect.y = round(self.xy_pos.y)


class PedestriansTimer:
    def __init__(self,
                 groups,
                 pedestrians_start_pos_no,
                 pos,
                 player,
                 distance_between_rects_method,
                 event_loop,
                 settings,
                 map_width,
                 map_height):

        # attributes for pedestrian-instantiation
        self.groups = groups
        self.pos = pos
        self.rect = pg.Rect((pos[0], pos[1]), (50, 50))
        self.player = player
        self.check_distance_between_rects = distance_between_rects_method
        self.settings = settings
        self.map_width = map_width
        self.map_height = map_height

        self.pedestrians_start_pos_no = pedestrians_start_pos_no
        self.event_name = f'pedestrians_timer_{self.pedestrians_start_pos_no}'
        self.event_loop = event_loop

        self.spawn_times = (1000, 1250, 1500, 1750, 2000, 2250, 2500)
        self.timer_set = False
        self.random_renew_timer_timestamp = pg.time.get_ticks()

        self.last_pedestrian_numbers = []

    def set_pedestrians_timer(self):
        self.event_id = pg.USEREVENT + 3 + self.pedestrians_start_pos_no
        self.event_loop.EVENT_IDS[self.event_name] = self.event_id
        pg.time.set_timer(self.event_id, rnd.choice(self.spawn_times))
        self.event_loop.add_event(self.event_id)

    def drop_pedestrians_timer(self):
        if self.event_name in self.event_loop.EVENT_IDS.keys():
            self.event_loop.remove_event(self.event_loop.EVENT_IDS[self.event_name])
            del self.event_loop.EVENT_IDS[self.event_name]
            del self.event_id

    def is_timer_set(self):
        if self.check_distance_between_rects(rect1=self.rect, rect2=self.player.rect, max_distance=3400):
            if not self.timer_set:
                self.set_pedestrians_timer()
                self.timer_set = True
        else:
            self.drop_pedestrians_timer()
            self.timer_set = False

    def renew_randomly_timer_timer(self):
        if rnd.randint(0,100) > 95:
            if self.timer_set:
                self.drop_pedestrians_timer()
                self.set_pedestrians_timer()
                self.random_renew_timer_timestamp = pg.time.get_ticks()

    def spawn_pedestrian(self):
        if hasattr(self, 'event_id'):
            if self.event_name in self.event_loop.triggered_events:

                if len(self.last_pedestrian_numbers) > 3:
                    self.last_pedestrian_numbers.pop(0)

                pedestrian_number = rnd.randint(1,10)

                while pedestrian_number in self.last_pedestrian_numbers:
                    pedestrian_number = rnd.randint(1,10)

                self.last_pedestrian_numbers.append(pedestrian_number)
                
                Pedestrian(groups=self.groups,
                    pos=self.pos,
                    pedestrian_line=self.pedestrians_start_pos_no,
                    pedestrian_no=pedestrian_number,
                    player=self.player,
                    settings=self.settings,
                    map_width=self.map_width,
                    map_height=self.map_height,
                    distance_between_rects_method=self.check_distance_between_rects)
                self.event_loop.triggered_events.remove(self.event_name)

    def update(self):
        self.is_timer_set()
        if self.timer_set:
            self.spawn_pedestrian()

        # every 3 seconds, renew with a 5% chance the pedestrians spawn timer for a different spawn time interval
        if pg.time.get_ticks() - self.random_renew_timer_timestamp > 3000:
            self.renew_randomly_timer_timer()
