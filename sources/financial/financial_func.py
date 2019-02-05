import os
import sys
import datetime
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.dirname(FILE_DIR)
FIN_DIR = os.path.join(SRC_DIR, 'financial')
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
sys.path.append(FIN_DIR)
sys.path.append(SRC_DIR)
from util import util
from util import logger
from database.ft_db import get_firstrade_db
from financial_basics import xirr
LOGGER = logger.get_single_logger()
CONFIG = util.loadConfig(os.path.join(DATA_DIR, 'config.json'))
DB = get_firstrade_db(db_fpath=os.path.join(DATA_DIR, CONFIG['database']))

def calcAnnualizedReturn(symbol, current_price):
    LOGGER.debug('given: {}:{}'.format(symbol, current_price))
    ret = DB.readBySymbol(symbol)
    total_Quantity = 0
    total_cost = 0
    cashflows = []
    for r in ret:
        LOGGER.debug(r)
        total_Quantity += r.Quantity
        if r.Action == 'buy':
            total_cost += r.Amount
            cashflows.extend([(r.TradeDate, r.Amount)])

    LOGGER.debug('total_Quantity: {}'.format(total_Quantity))
    LOGGER.debug('total_cost: {}'.format(total_cost))
    cashflows.extend([(datetime.datetime.today(), total_Quantity * current_price)])
    LOGGER.debug('cashflows: {}'.format(cashflows))
    AnnualizedReturn = xirr(cashflows)
    LOGGER.debug('AnnualizedReturn: {}'.format(AnnualizedReturn))
    return AnnualizedReturn
