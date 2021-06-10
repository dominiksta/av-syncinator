from enum import Enum
import traceback

instance = None

class LogLvl(Enum):
    INFO = 0,
    DEBUG = 1,
    WARN = 2,
    ERROR = 3,


class Logger:
    @staticmethod
    def get_instance():
        global instance
        if instance == None: instance = Logger()
        return instance


    def __init__(self):
        self.lvl = LogLvl.INFO
        self.output_function = print


    def log(self, lvl: LogLvl, msg: str):
        msg = '[{lvl}]: {msg}'.format(lvl = lvl.name, msg = msg)

        if lvl.value >= self.lvl.value:
            if lvl == lvl.ERROR:
                self.output_function(msg + '\nTraceback: ' +
                                     traceback.format_exc())
            else:
                self.output_function(msg)


    def info(self, msg: str): return self.log(LogLvl.INFO, msg)
    def debug(self, msg: str): return self.log(LogLvl.DEBUG, msg)
    def warn(self, msg: str): return self.log(LogLvl.WARN, msg)
    def error(self, msg: str): return self.log(LogLvl.ERROR, msg)