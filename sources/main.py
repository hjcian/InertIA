# -*- coding: utf-8 -*-
import os
import sys
import csv
from docopt import docopt
from database.ft_db import FirstradeDB
FTDB = FirstradeDB()

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
    fpath = sys.argv[1]
    readFirstradeCSV(fpath)
    ret = FTDB.queryAll()
    for row in ret:
        print(row)