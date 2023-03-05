
from code.game_loop import GameLoop

from code.logger import Logger
import logging


# init of game_loop object and running loop
if __name__ == "__main__":
    try:
        game_loop = GameLoop()
        game_loop.looping()
    except Exception as e:
        Logger()
        logging.exception(e)
        raise Exception(e)
