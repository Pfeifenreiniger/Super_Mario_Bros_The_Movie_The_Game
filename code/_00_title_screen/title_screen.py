
import pygame as pg


class TitleScreen:
    def __init__(self, event_loop):
        self.screen = pg.display.get_surface()

        # event loop - adding a custom event
        self.event_loop = event_loop
        clouds_timer = pg.event.custom_type()
        pg.time.set_timer(clouds_timer, 12 * 1000)
        self.event_loop.add_event(clouds_timer)

        # inst objects
        self.sky = Sky(self.screen)
        self.dinohattan = Dinohattan(self.screen)
        self.koopahari_desert = KoopahariDesert(self.screen)
        self.clouds = pg.sprite.Group()
        self.cloud_numb = 1
        Cloud(group=self.clouds, cloud_numb=self.cloud_numb)
        self.logo = Logo(self.screen)
        self.logo_appearance = False
        self.press_start = PressStart(self.screen)

        self.button_pressed = False
        self.button_pressed_timestamp = None

        # music
        self.music = pg.mixer.Sound("../audio/music/Walk_the_Dinosaur_(GXSCC_Gameboy_Mix).ogg")
        self.music.play(loops=-1)

    def check_logo_appearance(self):
        if not self.logo_appearance:
            if pg.time.get_ticks() - self.logo.inst_time > 4500:
                self.logo_appearance = True

    def input(self):

        if not self.button_pressed:
            keys = pg.key.get_pressed()

            if keys[pg.K_SPACE] or keys[pg.K_RETURN]:
                if not self.logo_appearance:
                    self.logo_appearance = True
                if self.logo.xy_pos.y < 68:
                    self.logo.xy_pos.y = 68
                    self.logo.rect.y = round(self.logo.xy_pos.y)
                else:
                    print("Let's start the game!!!")
                self.button_pressed = True
                self.button_pressed_timestamp = pg.time.get_ticks()
        else:
            if pg.time.get_ticks() - self.button_pressed_timestamp > 300:
                self.button_pressed = False

    def update(self, dt):

        self.input()

        self.check_logo_appearance()

        self.dinohattan.update(dt)
        self.koopahari_desert.update(dt)

        if self.event_loop.loop_events() == "spawn_cloud":
            self.cloud_numb = 1 if self.cloud_numb == 2 else 2
            Cloud(group=self.clouds, cloud_numb=self.cloud_numb)

        for cloud in self.clouds:
            cloud.update(dt)

        if self.logo_appearance:
            self.logo.update(dt)

        self.draw()


    def draw(self):
        self.sky.draw()

        for cloud in self.clouds:
            self.screen.blit(cloud.image, cloud.rect)


        self.dinohattan.draw()
        self.koopahari_desert.draw()

        if self.logo_appearance:
            self.logo.draw()

        if self.logo.xy_pos.y >= 68:
            self.press_start.draw()



class KoopahariDesert:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load("../graphics/title_screen/koopahari_desert.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=0, y=80)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed = 200

    def move(self, dt):
        if self.xy_pos.x <= -2350:
            self.xy_pos.x = 0
            self.rect.x = self.xy_pos.x
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)
        else:
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Dinohattan:
    def __init__(self, screen):
        self.screen = screen
        self.image_front = pg.image.load("../graphics/title_screen/dinohattan_front.png").convert_alpha()
        self.xy_front = pg.math.Vector2(x=0, y=64)
        self.rect_front = self.image_front.get_rect(topleft = self.xy_front)
        self.image_back = pg.image.load("../graphics/title_screen/dinohattan_back.png").convert_alpha()
        self.xy_back = pg.math.Vector2(x=0, y=251)
        self.rect_back = self.image_back.get_rect(topleft = self.xy_back)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed_front = 150
        self.speed_back = 100

    def move(self, dt):
        # front
        if self.xy_front.x <= -1428:
            self.xy_front.x = 0
            self.rect_front.x = self.xy_front.x
            self.xy_front.x += self.direction.x * self.speed_front * dt
            self.rect_front.x = round(self.xy_front.x)
        else:
            self.xy_front.x += self.direction.x * self.speed_front * dt
            self.rect_front.x = round(self.xy_front.x)

        # back
        if self.xy_back.x <= -1600:
            self.xy_back.x = 0
            self.rect_back.x = self.xy_back.x
            self.xy_back.x += self.direction.x * self.speed_back * dt
            self.rect_back.x = round(self.xy_back.x)
        else:
            self.xy_back.x += self.direction.x * self.speed_back * dt
            self.rect_back.x = round(self.xy_back.x)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.screen.blit(self.image_back, self.rect_back)
        self.screen.blit(self.image_front, self.rect_front)

class Sky:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load("../graphics/title_screen/sky.png").convert()
        self.xy_pos = pg.math.Vector2(x=0, y=0)
        self.rect = self.image.get_rect(topleft=self.xy_pos)

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Cloud(pg.sprite.Sprite):
    def __init__(self, group, cloud_numb:int):
        super().__init__(group)
        self.image = pg.image.load(f"../graphics/title_screen/clouds_{cloud_numb}.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=800, y=87) if cloud_numb == 1 else pg.math.Vector2(x=800, y=93)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        # float based movement
        self.direction = pg.math.Vector2(x=-1, y=0)
        self.speed = 50

    def move(self, dt):
        if self.rect.right <= 0:
            self.kill()
        else:
            self.xy_pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.xy_pos.x)

    def update(self, dt):
        self.move(dt)

class Logo:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load("../graphics/title_screen/logo.png").convert_alpha()
        self.xy_pos = pg.math.Vector2(x=166, y=-193)
        self.rect = self.image.get_rect(topleft = self.xy_pos)

        self.inst_time = pg.time.get_ticks()

        # float based movement
        self.direction = pg.math.Vector2(x=0, y=1)
        self.speed = 100

    def move(self, dt):
        if self.xy_pos.y < 68:
            self.xy_pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.xy_pos.y)

    def update(self, dt):
        self.move(dt)

    def draw(self):
        self.screen.blit(self.image, self.rect)


class PressStart:
    def __init__(self, screen):
        self.screen = screen
        font = pg.font.Font("../graphics/fonts/masheen/masheen_bold.ttf", 30)
        text = "PRESS START"
        self.text_surf =  font.render(text, True, (244, 244, 244))
        self.text_rect = self.text_surf.get_rect(center = (400, 510))

        self.blink_value = -1

    def slow_blink(self):
        self.blink_value += 0.06
        if self.blink_value > 1: self.blink_value = -1

        if self.blink_value >= 0: return True
        else: return False

    def draw(self):
        if self.slow_blink():
            self.screen.blit(self.text_surf, self.text_rect)
