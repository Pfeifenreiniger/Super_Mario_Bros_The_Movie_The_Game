
import pygame as pg
import os
import sys
import sqlite3
import pandas as pd

class SavegameDB:
    def __init__(self):
        self.db = self.__connect_to_db()
        self.__create_table()

    def __connect_to_db(self):
        tries = 0

        exc = ""

        while tries <= 3:
            try:
                # checks if 00_saves folder is present
                if "00_saves" not in os.listdir('data/'):
                    os.mkdir('data/00_saves/')

                saves_db = sqlite3.connect('data/00_saves/savegames.db')

                cursor_t = saves_db.cursor()
                cursor_t.close()

                break
            except Exception as e:
                tries += 1
                exc = e

        if tries > 3:
            raise Exception("Exception in creating/connection to savegames.db.\n" + exc)
        else:
            return saves_db

    def __create_table(self):
        """creates table and fills it with standard values (id 0) if not already present"""

        cursor = self.db.cursor()

        query = f"""
                CREATE TABLE IF NOT EXISTS saves
                (
                [level] INTEGER
                )
                ;
                """

        cursor.execute(query)

        query = f"""
                INSERT OR IGNORE INTO saves
                (
                level
                )
                VALUES
                (
                0
                )
                ;
                """

        cursor.execute(query)

        self.db.commit()
        cursor.close()

    def load_level(self) -> int:

        query = """
                SELECT * FROM saves
                """

        cursor = self.db.cursor()

        cursor.execute(query)

        saves_df = pd.DataFrame(cursor.fetchone(), columns=['saves'])

        cursor.close()

        return int(saves_df['saves'][0])

    def update_level(self, level:int):

        old_lvl = self.load_level()

        query = f"""
                UPDATE saves
                SET level = {level}
                WHERE level = {old_lvl}
                ;
                """

        cursor = self.db.cursor()

        cursor.execute(query)

        self.db.commit()

        cursor.close()


