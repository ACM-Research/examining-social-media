offset = 0
limit = 3000
period = '4y'

import pandas as pd

import yfinance as yf
import os, contextlib
import shutil
from os.path import isfile, join

data = yf.download("NFLX", period=period)
data.to_csv('C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/{}.csv'.format("NFLX"))


def move_symbols(symbols, dest):
    for s in symbols:
        filename = '{}.csv'.format(s)
        shutil.move(join('hist', filename), join(dest, filename))


#move_symbols(etfs, "etfs")
#move_symbols(stocks, "stocks")


