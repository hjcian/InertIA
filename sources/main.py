# -*- coding: utf-8 -*-
import os
import sys
from docopt import docopt
from database.ft_db import get_firstrade_db
from util import util
from util import logger
from financial import financial_func
DOCOPT_DOC = """
Usage: 
    {0} (-h)
    {0} [--import <filepath>]
        [--calc <symbol:price>]

Options:
    -h                      Show this help.
    --import <filepath>     Read file from <file path>.
                            Allowed format: 
                                1. Firstrade standard account historical record csv file
    --calc <symbol:price>   Calculate Annual Return by given symbol and current (today) price.
                            Allowed format: 
                                1. VT:70.1

""".format(os.path.basename(__file__))

SRC_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CONFIG = util.loadConfig(os.path.join(DATA_DIR, 'config.json'))
FTDB = get_firstrade_db(db_fpath=os.path.join(DATA_DIR, CONFIG['database']))
LOGGER = logger.get_single_logger()

def importData(fpath):
    FTStandardCSV = fpath
    FTDB.importFTStandardCSV(FTStandardCSV)
    ret = FTDB.queryAll()
    for row in ret:
        LOGGER.info(row)

def _parseSymbolPrice(symbolAndPrice):
    s_p = symbolAndPrice.split(':')
    if len(s_p) != 2:
        raise KeyError('Foramt error ({})'.format(symbolAndPrice))
    try:
        symbol = s_p[0].lower()
        price = float(s_p[1])
        return symbol, price
    except Exception as err:
        raise KeyError('Foramt error ({}:{}): {}'.format(symbol, price, err))

if __name__ == "__main__":
    argv = docopt(DOCOPT_DOC)
    if argv['--import']:
        importData(argv['--import'])
    elif argv['--calc']:
        symbol, price = _parseSymbolPrice(argv['--calc'])
        financial_func.calcAnnualizedReturn(symbol, price)

    

 