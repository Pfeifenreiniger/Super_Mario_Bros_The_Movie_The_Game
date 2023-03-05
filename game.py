
from code.game_loop import GameLoop


# init of game_loop object and running loop
if __name__ == "__main__":
    try:
        game_loop = GameLoop()
        game_loop.looping()
    except Exception as e:

        from code.logger import Logger
        import logging

        Logger()
        logging.exception(e)
        raise Exception(e)
