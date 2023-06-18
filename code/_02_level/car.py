
import pygame as pg
import random as rnd

from code._02_level.entity import Entity

class Car(Entity):
    def __init__(self, groups, pos, model_no, car_no, player, settings, map_width, map_height, distance_between_rects_method):

        self.image = pg.image.load(f"graphics/02_streets_of_dinohattan/entities/cars/model{model_no}/model{model_no}_car{car_no}.png").convert_alpha()

        pos = self.randomize_y_pos(pos)

        super().__init__(groups=groups,
                         pos=pos,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.cars_sprites = groups[1]
        self.set_hitbox(pos)
        self.set_direction()

        self.base_speed = 280
        self.speed_variance = 4
        self.speed = self.base_speed + (rnd.randint(-self.speed_variance * 3, self.speed_variance * 3))

        self.player = player
        self.distance_to_player = 0 # value will be overwritten by check_distance method of player class

    def randomize_y_pos(self, pos:tuple[int, int]) -> tuple[int, int]:
        """To give the y-pos a bit of variance"""
        return (pos[0], pos[1] + rnd.randint(-4, 4))

    def set_hitbox(self, pos):
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect

    def set_direction(self):
        if self.xy_pos.x < 600: # moving to the right
            self.direction.x = 1

        else: # moving to the left
            self.direction.x = -1
            self.image = pg.transform.flip(self.image, True, False)

    def check_player_collision(self):
        if self.distance_to_player <= 150:
            if self.hitbox.colliderect(self.player.rect):
                self.player.lose_life()

    def check_car_collision(self):
        for sprite in self.cars_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                if self.direction.x == 1:
                    if self.hitbox.left < sprite.hitbox.left and abs(self.hitbox.centery - sprite.hitbox.centery) < 6:
                        self.speed -= self.speed_variance
                    else:
                        self.speed += self.speed_variance
                else:
                    if self.hitbox.right > sprite.hitbox.right and abs(self.hitbox.centery - sprite.hitbox.centery) < 6:
                        self.speed -= self.speed_variance
                    else:
                        self.speed += self.speed_variance

    def update(self, dt):
        self.move(dt)
        self.hitbox = self.rect

        self.check_car_collision()
        self.check_player_collision()

        if not -200 < self.rect.x < 3400:
            self.kill()


class CarsTimer:
    def __init__(self, groups,
                 cars_start_pos_no,
                 pos,
                 player,
                 distance_between_rects_method,
                 event_loop,
                 settings,
                 map_width,
                 map_height):

        # attributes for car-instantiation
        self.groups = groups
        self.pos = pos
        self.rect = pg.Rect((pos[0], pos[1]), (50, 50))
        self.player = player
        self.check_distance_between_rects = distance_between_rects_method
        self.settings = settings
        self.map_width = map_width
        self.map_height = map_height

        self.cars_start_pos_no = cars_start_pos_no
        self.event_name = f'cars_timer_{self.cars_start_pos_no}'
        self.event_loop = event_loop

        self.spawn_times = (1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000)
        self.timer_set = False
        self.random_renew_timer_timestamp = pg.time.get_ticks()

    def set_cars_timer(self):
        self.event_id = pg.USEREVENT + 2 + self.cars_start_pos_no
        self.event_loop.EVENT_IDS[self.event_name] = self.event_id
        pg.time.set_timer(self.event_id, rnd.choice(self.spawn_times))  # every one and half a second a car spawn
        self.event_loop.add_event(self.event_id)

    def drop_cars_timer(self):
        if self.event_name in self.event_loop.EVENT_IDS.keys():
            self.event_loop.remove_event(self.event_loop.EVENT_IDS[self.event_name])
            del self.event_loop.EVENT_IDS[self.event_name]
            del self.event_id

    def is_timer_set(self):
        if self.check_distance_between_rects(rect1=self.rect, rect2=self.player.rect, max_distance=3400):
            if not self.timer_set:
                self.set_cars_timer()
                self.timer_set = True
        else:
            self.drop_cars_timer()
            self.timer_set = False

    def renew_randomly_cars_timer(self):
        if rnd.randint(0,100) > 95:
            if self.timer_set:
                self.drop_cars_timer()
                self.set_cars_timer()
                self.random_renew_timer_timestamp = pg.time.get_ticks()

    def spawn_car(self):
        if hasattr(self, 'event_id'):
            if self.event_name in self.event_loop.triggered_events:
                Car(groups=self.groups,
                    pos=self.pos,
                    model_no=rnd.randint(1,4),
                    car_no=rnd.randint(1,3),
                    player=self.player,
                    settings=self.settings,
                    map_width=self.map_width,
                    map_height=self.map_height,
                    distance_between_rects_method=self.check_distance_between_rects)
                self.event_loop.triggered_events.remove(self.event_name)

    def update(self):
        self.is_timer_set()
        if self.timer_set:
            self.spawn_car()

        # every 3 seconds, renew with a 5% chance the cars spawn timer for a different spawn time interval
        if pg.time.get_ticks() - self.random_renew_timer_timestamp > 3000:
            self.renew_randomly_cars_timer()
