
import time
import yfinance as yf
import dateutil.relativedelta
import matplotlib.pyplot as plt
from datetime import date, timedelta
import datetime
import numpy as np

import config
import sys

import os.path

class DataCollector():
        
    def __init__(self):
        pass

    def getStockData(ticker):
        #global MONTH_CUTTOFF
        currentDate = datetime.datetime.strptime(
        date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - \
        dateutil.relativedelta.relativedelta(months=config.MONTH_CUTTOFF)
        sys.stdout = open(os.devnull, "w")
        data = yf.download(ticker, pastDate, currentDate)
        sys.stdout = sys.__stdout__
        return data


    def getData(ticker):
        currentDate = datetime.datetime.strptime(
        date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - \
        dateutil.relativedelta.relativedelta(months=config.MONTH_CUTTOFF)
        sys.stdout = open(os.devnull, "w")
        data = yf.download(ticker, pastDate, currentDate)
        sys.stdout = sys.__stdout__
        return data[["Volume"]]


