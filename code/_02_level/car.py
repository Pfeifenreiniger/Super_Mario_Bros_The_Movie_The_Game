
import pygame as pg
import random as rnd

from code._02_level.entity import Entity

class Car(Entity):
    def __init__(self,
                 groups,
                 pos,
                 car_line,
                 model_no,
                 car_no,
                 player,
                 settings,
                 map_width,
                 map_height,
                 distance_between_rects_method,
                 traffic_light):

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

        self.car_line = car_line
        self.traffic_light = traffic_light

        self.base_speed = 280
        self.speed_variance = 4
        self.speed = self.base_speed + (rnd.randint(-self.speed_variance * 3, self.speed_variance * 3))
        self.start_speed = self.speed
        self.max_speed = self.speed * 1.1

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
            if self.car_line == sprite.car_line:

                # reduce speed or stop if cars close to each other
                if (self.direction.x == 1 and self.hitbox.left < sprite.hitbox.left) \
                        or (self.direction.x == -1 and self.hitbox.right > sprite.hitbox.right):

                    if self.check_distance_between_rects(rect1=self.hitbox, rect2=sprite.hitbox, max_distance=225):
                        self.speed = 0
                    elif self.check_distance_between_rects(rect1=self.hitbox, rect2=sprite.hitbox, max_distance=300):
                        self.speed = int(self.speed / 2)
                    else: # if no cars in front, give speed!
                        if self.speed < self.max_speed:
                            self.speed += self.speed_variance

                # avoid cars overlapping
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction.x == 1: # moving to the right
                        if self.hitbox.left < sprite.hitbox.left:
                            self.speed = 0
                            self.hitbox.right = sprite.hitbox.left - 2
                    else: # moving to the left
                        if self.hitbox.right > sprite.hitbox.right:
                            self.speed = 0
                            self.hitbox.left = sprite.hitbox.right + 2

    def check_traffic_light(self):
        if self.car_line >= 14: # traffic light only for car lines 14 and 15
            speed_change = 15
            if self.rect.left >= self.traffic_light.rect.right + 167 \
                    and self.check_distance_between_rects(rect1=self.hitbox, rect2=self.traffic_light.rect, max_distance=550): # check traffic light if car is right to light signal

                if self.traffic_light.frame == 1: # red for cars
                    if self.speed - speed_change > 0:
                        self.speed -= speed_change
                    elif self.speed != 0:
                        self.speed = 0
                else: # green for cars
                    if self.speed != self.start_speed:
                        if self.speed + speed_change > self.start_speed:
                            self.speed = self.start_speed
                        else:
                            self.speed += speed_change
            elif self.speed != self.start_speed:
                if self.speed + speed_change > self.start_speed:
                    self.speed = self.start_speed
                else:
                    self.speed += speed_change

    def update(self, dt):
        self.move(dt)
        self.hitbox = self.rect

        self.check_car_collision()
        self.check_player_collision()
        self.check_traffic_light()

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
                 map_height,
                 traffic_light):

        # attributes for car-instantiation
        self.groups = groups
        self.pos = pos
        self.rect = pg.Rect((pos[0], pos[1]), (50, 50))
        self.player = player
        self.check_distance_between_rects = distance_between_rects_method
        self.settings = settings
        self.map_width = map_width
        self.map_height = map_height

        self.traffic_light = traffic_light

        self.cars_start_pos_no = cars_start_pos_no
        self.event_name = f'cars_timer_{self.cars_start_pos_no}'
        self.event_loop = event_loop

        self.spawn_times = (1750, 2000, 2250, 2500, 2750, 3000)
        self.timer_set = False
        self.random_renew_timer_timestamp = pg.time.get_ticks()

    def set_cars_timer(self):
        self.event_id = pg.USEREVENT + 2 + self.cars_start_pos_no
        self.event_loop.EVENT_IDS[self.event_name] = self.event_id
        pg.time.set_timer(self.event_id, rnd.choice(self.spawn_times))
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
                    car_line=self.cars_start_pos_no,
                    model_no=rnd.randint(1,4),
                    car_no=rnd.randint(1,3),
                    player=self.player,
                    settings=self.settings,
                    map_width=self.map_width,
                    map_height=self.map_height,
                    distance_between_rects_method=self.check_distance_between_rects,
                    traffic_light=self.traffic_light)
                self.event_loop.triggered_events.remove(self.event_name)

    def update(self):
        self.is_timer_set()
        if self.timer_set:
            self.spawn_car()

        # every 3 seconds, renew with a 5% chance the cars spawn timer for a different spawn time interval
        if pg.time.get_ticks() - self.random_renew_timer_timestamp > 3000:
            self.renew_randomly_cars_timer()
