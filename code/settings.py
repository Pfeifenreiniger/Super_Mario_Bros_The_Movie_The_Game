
import pygame as pg
import os
import sys
import sqlite3
import pandas as pd


class Settings:
    def __init__(self):

        settings_db = SettingsDB()
        self.db = settings_db.db

        self.get_settings()

        # screen hard settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.resolution = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.flags_window = pg.HWSURFACE|pg.DOUBLEBUF
        self.flags_fullscreen = pg.FULLSCREEN|pg.SCALED|pg.HWSURFACE|pg.DOUBLEBUF

    def get_settings(self):

        cursor = self.db.cursor()

        query = f"""
                SELECT * FROM settings
                """

        cursor.execute(query)

        settings_df = pd.DataFrame(cursor.fetchall(), columns=['settings_id', 'screen_mode', 'music_vol', 'sfx_vol'])

        if 1 in settings_df['settings_id']:
            settings = settings_df[settings_df['settings_id'] == 1]
        else:
            settings = settings_df[settings_df['settings_id'] == 0]

        self.screen_mode = settings['screen_mode'].item()
        self.music_volume = round(float(settings['music_vol'].item()), 1)
        self.sfx_volume = round(float(settings['sfx_vol'].item()), 1)

        cursor.close()

    def save_changes_to_db(self):

        cursor = self.db.cursor()

        query = f"""
                SELECT * FROM settings
                """

        cursor.execute(query)

        settings_df = pd.DataFrame(cursor.fetchall(), columns=['settings_id', 'screen_mode', 'music_vol', 'sfx_vol'])

        if 1 in settings_df['settings_id']:

            query = f"""
                    UPDATE settings
                    SET
                    screen_mode = '{self.screen_mode}',
                    music_vol = {self.music_volume},
                    sfx_vol = {self.sfx_volume}
                    WHERE
                    settings_id = 1
                    ;
                    """

        else:

            query = f"""
                    INSERT OR IGNORE INTO settings
                    (settings_id,
                    screen_mode,
                    music_vol,
                    sfx_vol)
                    VALUES
                    (1,
                    '{self.screen_mode}',
                    {self.music_volume},
                    {self.sfx_volume})
                    ;
                    """

        cursor.execute(query)
        self.db.commit()
        cursor.close()

    def get_display_screen(self):
        if self.screen_mode == "WINDOW":
            return pg.display.set_mode(self.resolution, self.flags_window, 8)
        else:
            return pg.display.set_mode(self.resolution, self.flags_fullscreen, 8)

    def increase_volume(self, music_or_sfx:str):

        # music
        if music_or_sfx.startswith("mus"):
            if self.music_volume < 1:
                self.music_volume += 0.1
                self.music_volume = round(self.music_volume, 1)
        # sfx
        else:
            if self.sfx_volume < 1:
                self.sfx_volume += 0.1
                self.sfx_volume = round(self.sfx_volume, 1)

    def decrease_volume(self, music_or_sfx:str):

        # music
        if music_or_sfx.startswith("mus"):
            if self.music_volume > 0:
                self.music_volume -= 0.1
                self.music_volume = round(self.music_volume, 1)
        # sfx
        else:
            if self.sfx_volume > 0:
                self.sfx_volume -= 0.1
                self.sfx_volume = round(self.sfx_volume, 1)


class SettingsDB:
    def __init__(self):
        self.db = self.__connect_to_db()
        self.__create_table()

    def __connect_to_db(self):
        tries = 0

        exc = ""

        while tries <= 3:
            try:
                # checks if 00_settings folder is present
                if "00_settings" not in os.listdir('data/'):
                    os.mkdir('data/00_settings/')

                settings_db = sqlite3.connect('data/00_settings/settings.db')

                cursor_t = settings_db.cursor()
                cursor_t.close()

                break
            except Exception as e:
                tries += 1
                exc = e

        if tries > 3:
            raise Exception("Exception in creating/connection to settings.db.\n" + exc)
        else:
            return settings_db

    def __create_table(self):
        """creates table and fills it with standard values (id 0) if not already present"""

        cursor = self.db.cursor()

        query = f"""
                CREATE TABLE IF NOT EXISTS settings
                ([settings_id] INTEGER PRIMARY KEY,
                [screen_mode] TEXT,
                [music_vol] REAL,
                [sfx_vol] REAL,
                UNIQUE(settings_id)
                )
                ;
                """

        cursor.execute(query)

        query = f"""
                INSERT OR IGNORE INTO settings
                (settings_id,
                screen_mode,
                music_vol,
                sfx_vol)
                VALUES
                (0,
                'WINDOW',
                1,
                1)
                ;
                """

        cursor.execute(query)

        self.db.commit()
        cursor.close()



