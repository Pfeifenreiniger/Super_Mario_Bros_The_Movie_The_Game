
import pygame as pg

from code._01_level.entity import Entity

class Enemy(Entity):
    def __init__(self, groups, pos, collision_sprites, death_zones, ledges, settings, map_width, player, distance_between_rects_method):
        super().__init__(groups, pos, collision_sprites, death_zones, settings, map_width, distance_between_rects_method)

        self.player = player

        self.aggro_range_x = 300
        self.aggro_range_y = 50

        self.ledges = ledges

        if self.__class__.__name__ == "Rat":
            dying_sfx = pg.mixer.Sound("audio/sfx/enemies/rat/rat_squeak_sfx.mp3")
        elif self.__class__.__name__ == "Bouncer":
            dying_sfx = pg.mixer.Sound("audio/sfx/enemies/bouncer/bouncer_get_koed.mp3")

        self.sfx = {
            "dying" : dying_sfx
        }

    def check_collision(self, direction):

        contact = False

        for sprite in self.collision_sprites.sprites():

            # check for tiles in 90 pixels distance to enemy
            if sprite.check_distance_between_rects(rect1=self.rect, rect2=sprite.rect, max_distance=90):

                # contact between enemy rect and floor, ceiling, and walls
                if sprite.rect.colliderect(self.rect):

                    if direction == "horizontal":
                        # left collision
                        if self.direction.x < 0:
                            if self.rect.left <= sprite.rect.right:
                                self.rect.left = sprite.rect.right
                        # right collision
                        elif self.direction.x > 0:
                            if self.rect.right >= sprite.rect.left:
                                self.rect.right = sprite.rect.left
                        self.xy_pos.x = self.rect.x
                    elif direction == "vertical":
                        # top collision
                        if self.rect.top <= sprite.rect.bottom:
                            if self.direction.y < 0:
                                self.rect.top = sprite.rect.bottom
                                self.rect.top = sprite.rect.bottom
                        # bottom collision
                        if self.rect.bottom >= sprite.rect.top:
                            if self.direction.y >= 0:
                                self.rect.bottom = sprite.rect.top
                                contact = True
                                self.on_floor = True
                        self.xy_pos.y = self.rect.y
                        self.direction.y = 0

        # no contact between rat and floor -> falling
        if not contact:
            self.on_floor = False

    def check_fall_death(self):

        if self.rect.collidelist(self.death_zones) >= 0:
            self.sfx["dying"].play()
            self.kill()

    def face_player(self):
        if self.rect.centerx < self.player.rect.centerx:
            self.animation_status = f"{'stand' if 'stand' in self.animation_status else 'run'}_right"
        else:
            self.animation_status = f"{'stand' if 'stand' in self.animation_status else 'run'}_left"

    def check_if_ledge(self) -> bool:

        for ledge in self.ledges:
            if self.rect.colliderect(ledge):
                # facing left at a ledge to the left
                if ledge.right >= self.rect.left and ledge.left <= self.rect.left and "left" in self.animation_status:
                    return True
                # facing right at a ledge to the right
                elif ledge.left <= self.rect.right and ledge.right >= self.rect.right and "right" in self.animation_status:
                    return True
                else:
                    return False
        return False


    def run_to_player(self):

        if "left" in self.animation_status: # player's x lower than enemy's
            if (self.rect.centerx - self.player.rect.centerx <= self.aggro_range_x) \
            and abs(self.rect.centery - self.player.rect.centery <= self.aggro_range_y) \
            and self.rect.left >= self.player.rect.right and not self.check_if_ledge():
                self.animation_status = "run_left"
                self.direction.x = -1
            else:
                self.animation_status = "stand_left"
                self.direction.x = 0
        else:
            if (self.player.rect.centerx - self.rect.centerx <= self.aggro_range_x) \
            and abs(self.rect.centery - self.player.rect.centery <= self.aggro_range_y) \
            and self.rect.right <= self.player.rect.left and not self.check_if_ledge():
                self.animation_status = "run_right"
                self.direction.x = 1
            else:
                self.animation_status = "stand_right"
                self.direction.x = 0

    def deal_damage(self):

        # when enemy's hitbox touches player's hitbox and player is not currently attacking -> player gets damage
        if self.rect.colliderect(self.player.rect) and not 'attack' in self.player.animation_status:
            self.player.get_damage(amount=self.attack_power)

    def get_damage(self, knockback:int):

        # if player attacks and has a attackbox which collides with the enemy's hitbox -> enemy receives damage
        if 'attack' in self.player.animation_status:
            if hasattr(self.player, 'attackbox'):
                if self.player.attackbox.colliderect(self.rect):
                    self.player.sfx["crowbar_swing"].stop()
                    self.player.sfx["crowbar_hit"].play()
                    self.health -= self.player.attack_power
                    del self.player.attackbox

                    if self.health <= 0:
                        self.sfx["dying"].play()
                        self.kill()
                    # if not dead, enemy will be knocked back by player's attack
                    else:
                        if "left" in self.animation_status:
                            self.xy_pos.x += knockback * self.player.attack_power
                        else:
                            self.xy_pos.x -= knockback * self.player.attack_power

    def animate(self, dt):

        def return_frame_rotation_power() -> int:
            if "attack" in self.animation_status:
                return 15
            elif "run" in self.animation_status:
                return 20
            else:
                return 3

        frame_rotation_power = return_frame_rotation_power()

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0
            if "run" in self.animation_status:
                self.run_frame_direction = 1

        if "stand" in self.animation_status:
            self.frame_index += frame_rotation_power * dt
            if int(self.frame_index) >= len(self.sprites[self.animation_status]):
                self.frame_index = 0

        elif "run" in self.animation_status:
            if self.run_frame_direction > 0:  # going forwards through tuple
                self.frame_index += frame_rotation_power * dt
                if self.frame_index >= len(self.sprites[self.animation_status]):
                    self.frame_index = len(self.sprites[self.animation_status]) - 1
                    self.run_frame_direction = -1
            else:  # going backwards through tuple
                self.frame_index -= frame_rotation_power * dt
                if self.frame_index < 0:
                    self.frame_index = 0
                    self.run_frame_direction = 1

        if self.animation_status != self.old_animation_status:
            self.frame_index = 0

        self.image = self.sprites[self.animation_status][int(self.frame_index)]

    def update(self, dt):
        self.old_animation_status = self.animation_status
        self.face_player()
        self.run_to_player()
        self.move(dt)
        self.animate(dt)
        self.deal_damage()
        self.get_damage()
        self.check_fall_death()
