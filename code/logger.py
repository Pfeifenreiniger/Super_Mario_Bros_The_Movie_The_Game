
import logging
import datetime as dt
import time
import os

class Logger:
    def __init__(self):

        dt_stamp = f"{dt.date.today().strftime('%Y-%m-%d')}_{dt.datetime.now().strftime('%H-%M-%S')}"

        self.logfile_name = "data/00_logs/exceptions_log_" + dt_stamp + ".log"

        self.__init_logger()

    def __init_logger(self):

        if "00_logs" not in os.listdir('data/'):
            os.mkdir('data/00_logs/')

        self.__cleanup_logs()

        logging.basicConfig(filename=self.logfile_name, format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    def __cleanup_logs(self):
        """deletes logs which are older than 14 days"""

        log_root = 'data/00_logs/'

        for log in os.listdir(log_root):

            # transforms last modification date into datetime-object
            last_mod = time.localtime(os.stat(log_root + log).st_mtime)
            last_mod = f"{last_mod.tm_year}-{'%02d' % (last_mod.tm_mon,)}-{'%02d' % (last_mod.tm_mday,)}"
            last_mod = dt.date.fromisoformat(last_mod)

            # date of today minus 14 days
            best_before = dt.date.today() - dt.timedelta(days=14)

            if best_before >= last_mod:
                os.remove(log_root + log)
