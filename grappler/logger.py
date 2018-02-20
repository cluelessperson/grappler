import logging
import datetime as dt
from . import config

logger = logging.getLogger()
logger.log(100, "TIMESTAMP, MODULE, LEVEL, MESSAGE")


class MyFormatter(logging.Formatter):
    converter=dt.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y%m%dT%H%M%S.%f")
        return s


console = logging.StreamHandler()
logger.addHandler(console)
formatter = MyFormatter(fmt='%(asctime)s, %(name)s, %(levelno)-2s, %(message)s')
console.setFormatter(formatter)
logger.setLevel(config.log_level)
logger.log(100, "LOG LEVEL {}".format(config.log_level))
