# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:21:58 2018

@author: MaxCian
"""
from datetime import datetime, timedelta
from googlefinance.client import get_price_data


def get_prices(stock_symbol:str, exchange_symbol:str, *,  year:int = None, month:int = None, day:int = None, interval:str = None):
    """
    --> is a function with keyword-only-parameter(arguments)

    a homemade wrapper for getting historical prices from google finance API
    followed interpretations are use 'Vanguard Total World Stock' ETF as example, the pair information is 'NYSEARCA: VT'
    and assume the present day is 2018/4/15 (we are not have that day prices)
    reference: https://www.google.com.tw/search?q=VT+stock

    :param stock_symbol: is the 'VT' part
    :param exchange_symbol: is the 'NYSEARCA' part
    :param year: interval of year. e.g. year=1 means the data will extracted from 2017/4/16 to 2018/4/14
    :param month: interval of month. e.g. month=1 means the data will extracted from 2018/3/16 to 2018/4/14
    :param day: interval of day. e.g. day=30 means the data will extracted from last 30 trading days (i.e. from 2018/3/3)
    :return: return a pandas dataframe
    """
    if year is not None:
        period = '{0}Y'.format(year)
    elif month is not None:
        period = '{0}M'.format(month)
    elif day is not None:
        period = '{0}d'.format(day)
    elif interval is not None:
        period = interval
    else:
        return None
    param = {
        'q': stock_symbol, # Stock symbol (ex: "AAPL" or "VT" or ".DJI")
        'x': exchange_symbol, # Stock exchange symbol on which stock is traded (ex: "NASD" or "NYSEARCA" or "INDEXDJX")
        'i': '86400',  # Interval size in seconds ("86400" = 1 day intervals)
        'p': period  # Period (Ex: "1Y" = 1 year; 10M = 10 months; 1d = 1 day)
    }
    # get price data (return pandas dataframe)
    return get_price_data(param)