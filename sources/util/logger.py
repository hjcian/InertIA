# -*- coding: utf-8 -*-
import os
import time
import logging
import logging.handlers
import sys
from datetime import datetime, timedelta

CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

def get_single_logger(log_path=None, logger_name="def", level=DEBUG, ttl_day=30):
    _logger = SingletonLogger(log_path, logger_name, level, ttl_day)
    logger = _logger.getLogger()
    return logger

def create_logger(log_path=None, logger_name="def", level=DEBUG, ttl_day=30):
    _logger = Logger(log_path, logger_name, level, ttl_day)
    logger = _logger.getLogger()
    return logger

def change_level(logger, level='debug'):
    '''
    available levels: https://docs.python.org/3/library/logging.html#levels
    '''
    levels = {
        'CRITICAL': CRITICAL,
        'ERROR': ERROR, 
        'WARNING': WARNING,
        'INFO':	INFO,
        'DEBUG': DEBUG,
        'NOTSET': NOTSET
    }
    logger.setLevel(levels.get(level.upper(), DEBUG))
    logger.info("[LOGGER] change log level to {0}".format(level.upper()))

class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, dir_log, ttl_day, log_name):
        self.dir_log = dir_log
        self.ttl_day = ttl_day
        self.serv_name = log_name # 3-letters
        filename = self._makeLogFilename() # never to be with os.sep on the end!!!
        # filename = self.dir_log + self.serv_name + time.strftime("%Y%m%d") + ".log" #dir_log here MUST be with os.sep on the end
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when='midnight', interval=1, backupCount=0, encoding=None)

    def _makeLogFilename(self):
        return os.path.join(self.dir_log, '{0}{1}.log'.format(self.serv_name, time.strftime("%Y%m%d")))

    def clean(self):
        clean_day = datetime.now() - timedelta(days=self.ttl_day)
        clean_file = "{0}{1}{2}.log" \
            .format(self.dir_log, self.serv_name, clean_day.strftime("%Y%m%d"))
        if os.path.isfile(clean_file):
            os.remove(clean_file)

    def doRollover(self):
        self.stream.close()
        self.clean()
        self.baseFilename = self._makeLogFilename()
        self.stream = open(self.baseFilename, 'w')
        self.rolloverAt = self.rolloverAt + self.interval

class Logger():
    def __init__(self, log_path=None, logger_name="def", level=DEBUG, ttl_day=30):
        self._init_logger(log_path, logger_name, level, ttl_day)

    def _init_logger(self, log_path, logger_name, level, ttl_day):
        self._LOGGER = logging.getLogger(logger_name)
        self._LOGGER.setLevel(level)        
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        if log_path:
            self._makeDir(log_path)
            suffix = "{0}%Y%m%d.log".format(logger_name)
            handler = TimedRotatingFileHandler(log_path, ttl_day, logger_name)
            handler.setFormatter(formatter)
            handler.suffix = suffix
            self._LOGGER.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self._LOGGER.addHandler(console)
        self._LOGGER.info("Logger Initializing...")
        self._LOGGER.info("Current execution path: {0}".format(os.getcwd()))

    def _makeDir(self, dir_path):
        if not (os.path.exists(dir_path) and os.path.isdir(dir_path)):
            os.makedirs(dir_path)

    def getLogger(self):
        return self._LOGGER

class SingletonLogger(object):
    __instance = None

    class __SingletonLogger(Logger):
        pass

    def __new__(self, *args, **kwargs):
        if SingletonLogger.__instance is None:
             SingletonLogger.__instance = SingletonLogger.__SingletonLogger(*args, **kwargs)
        return SingletonLogger.__instance
