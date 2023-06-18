
import pygame as pg
import sys


class EventLoop:
    def __init__(self, settings):

        self.EVENT_IDS = {
                            "pg.QUIT" : pg.QUIT
                        }

        self.events = [pg.QUIT]
        pg.event.set_allowed(self.events)

        self.settings = settings

        self.triggered_events = []

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

                    # pg.QUIT
                    if my_event == self.EVENT_IDS.get("pg.QUIT"):
                        self.settings.db.close()
                        pg.quit()
                        sys.exit()

                    # _00_title_screen._00_main.CloudsTimerEvent
                    if my_event == self.EVENT_IDS.get('clouds_timer'):
                        self.triggered_events.append('clouds_timer')

                    # _02_level.car.CarsTimer
                    for event_name, event_id in self.EVENT_IDS.items():
                        if my_event == event_id:
                            self.triggered_events.append(event_name)


    def check_for_event(self, event_id:int) -> bool:
        for my_events in self.events:
            if my_events == event_id:
                return True
