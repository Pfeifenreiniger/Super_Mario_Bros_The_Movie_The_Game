
from code._02_level.entity import Entity

class Humanoid(Entity):
    def __init__(self, groups, pos, collision_sprites, settings, map_width, map_height, distance_between_rects_method):
        super().__init__(groups=groups,
                         pos=pos,
                         collision_sprites=collision_sprites,
                         settings=settings,
                         map_width=map_width,
                         map_height=map_height,
                         distance_between_rects_method=distance_between_rects_method)

        self.health = 100

        self.frame_index = 0
        self.frame_rotation_power = 7

        self.animation_status = "stand_up"
        self.old_animation_status = self.animation_status

        self.run_frame_direction = 1

    def is_idle_animation(self):
        if self.direction.x == 0 and self.direction.y == 0 and not 'stand' in self.animation_status:
            if 'up' in self.animation_status:
                self.animation_status = 'stand_up'
            elif 'down' in self.animation_status:
                self.animation_status = 'stand_down'
            elif 'left' in self.animation_status:
                self.animation_status = 'stand_left'
            elif 'right' in self.animation_status:
                self.animation_status = 'stand_right'

    def check_frame_rotation_power(self):
        if "run" in self.animation_status:
            self.frame_rotation_power = 9
        else:
            self.frame_rotation_power = 6

    def animate(self, dt):

        self.check_frame_rotation_power()

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if "run" in self.animation_status:

            if self.run_frame_direction > 0:  # going forward through tuple
                self.frame_index += self.frame_rotation_power * dt
                if self.frame_index >= len(self.sprites[self.animation_status]):
                    self.frame_index = len(self.sprites[self.animation_status]) - 1
                    self.run_frame_direction = -1
            else:  # going backwards through tuple
                self.frame_index -= self.frame_rotation_power * dt
                if self.frame_index < 0:
                    self.frame_index = 0
                    self.run_frame_direction = 1

        else:
            self.frame_index += self.frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites[self.animation_status]):
                self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]

