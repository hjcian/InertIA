# -*- coding: utf-8 -*-
import os
import sys
import csv
from docopt import docopt
from database.ft_db import FirstradeDB
from util import util
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CONFIG = util.loadConfig(os.path.join(DATA_DIR, 'config.json'))
FTDB = FirstradeDB(db_fpath=os.path.join(DATA_DIR, CONFIG['database']))

def fcn(*args, **kwargs):
    print('args: {}'.format(args))
    print('kwargs: {}'.format(kwargs))

def readFirstradeCSV(fpath):
    print(fpath)
    with open(fpath, 'r') as fp:
        csv_reader = csv.DictReader(fp)
        for row in csv_reader:
            FTDB.write(**row)

if __name__ == "__main__":
    pass
    fpath = sys.argv[1]
    readFirstradeCSV(fpath)
    ret = FTDB.queryAll()
    for row in ret:
        print(row)