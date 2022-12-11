
import pygame as pg
import sys

class EventLoop:
    def __init__(self):
        self.events = [pg.QUIT]
        pg.event.set_allowed(self.events)

    def add_event(self, event):
        if event not in self.events:
            self.events.append(event)
            pg.event.set_allowed(self.events)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)
            pg.event.set_allowed(self.events)

    def loop_events(self):
        for event in pg.event.get():

            for my_event in self.events:

                if event.type == my_event:

                    # print(my_event)

                    # pg.QUIT
                    if my_event == 256:
                        pg.quit()
                        sys.exit()

                    # title screen clouds_timer
                    if my_event == 32851:
                        return "spawn_cloud"

