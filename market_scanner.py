import os
import time
import yfinance as yf
import dateutil.relativedelta
import matplotlib.pyplot as plt
from datetime import date, timedelta
import datetime
import numpy as np
import sys
from stocklist import NasdaqController
from RSI_Calc import *
from tqdm import tqdm
from joblib import Parallel, delayed, parallel_backend
import multiprocessing
import smtplib
import email.utils
from EmailResults import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config
import sys
from RSI_Calc import *
from EMA_Calc import *
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pi/Documents/Stock_analyzer_bot')



###########################
# THIS IS THE MAIN SCRIPT #
###########################

class mainObj:

    def __init__(self):
        pass

    def getStockData(self, ticker):
        #global MONTH_CUTTOFF
        currentDate = datetime.datetime.strptime(
        date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - \
            dateutil.relativedelta.relativedelta(months=config.MONTH_CUTTOFF)
        sys.stdout = open(os.devnull, "w")
        data = yf.download(ticker, pastDate, currentDate)
        sys.stdout = sys.__stdout__
        return data


    def getData(self, ticker):
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        pastDate = currentDate - \
            dateutil.relativedelta.relativedelta(months=config.MONTH_CUTTOFF)
        sys.stdout = open(os.devnull, "w")
        data = yf.download(ticker, pastDate, currentDate)
        sys.stdout = sys.__stdout__
        return data[["Volume"]]

    def affordable(self, ticker):
        tick = yf.Ticker(ticker)
        tickHistory = tick.history(period="1d")
        if tickHistory["Close"].any():
            price = tickHistory["Close"][0]
            print(str(price))
            if price < 10:
                print("Affordable")
                return True
            else:
                print("Not worth it")
                return False
        else:
            return False

    def find_anomalies(self, data, currentDate):
        data_std = np.std(data['Volume'])
        data_mean = np.mean(data['Volume'])
        anomaly_cut_off = data_std * config.STD_CUTTOFF
        upper_limit = data_mean + anomaly_cut_off
        upper_limit=100
        data.reset_index(level=0, inplace=True)
        is_outlier = data['Volume'] > upper_limit
        is_in_three_days = ((currentDate - data['Date']) <= datetime.timedelta(days=config.DAY_CUTTOFF))
        return data[is_outlier & is_in_three_days]

    def customPrint(self, d, tick, RSI):
        print("\n\n\n*******  " + tick.upper() + "  *******")
        print("Ticker: "+tick.upper())
        print(d.to_string(index=False))
        print("RSI: "+str(RSI))
        print("*********************\n\n\n")

    def getRSI(self, data):
        ticker_df = data.reset_index()
        df = ticker_df
        df['RSI'] = RSI_Calc.computeRSI(df['Adj Close'], config.DAYS_OF_RSI)
        print("\n"+ str(df.iloc[-1]["RSI"]))
        return df

    def parallel_wrapper(self,x, currentDate, positive_scans):
        Stock_data = self.getStockData(x)
        d = (self.find_anomalies(Stock_data[["Volume"]], currentDate))
        config.DAYS_OF_RSI=14
        if d.empty:
            return
        df = self.getRSI(Stock_data)
        RSI = df.iloc[-1]["RSI"]
        print("\n"+ str(df.iloc[-1]["RSI"]))
        RSI_Calc.RSI_Graph(df)
        self.customPrint(d, x, RSI)
        if(config.SEND_EMAIL):
            EmailResults.SendResults(x, d, RSI)
        #Allows you to keep all data for the end of the Bots run. Not doing anything with it yet
        stonk = dict()
        stonk['Ticker'] = x
        stonk['TargetDate'] = d['Date'].iloc[0]
        stonk['TargetVolume'] = d['Volume'].iloc[0]
        stonk['RSI'] = RSI
        positive_scans.append(stonk)
        
    def main_func(self):
        positive_scans=True
        StocksController = NasdaqController(True)
        list_of_tickers = StocksController.getList()
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        start_time = time.time()
        if(config.SEND_EMAIL):
            #EmailResults.SendMessage("Bot started working", "BOT LOG")
            pass
            
        else:
            print("Bot started working")   

        manager = multiprocessing.Manager()
        positive_scans = manager.list()


        if(config.RUN_BOT):
            with parallel_backend('loky', n_jobs=multiprocessing.cpu_count()):
                Parallel()(delayed(self.parallel_wrapper)(x, currentDate, positive_scans)
                           for x in tqdm(list_of_tickers, miniters=1))
        else:
            #This is to debug main process with just one stock
            print(f)
            self.parallel_wrapper("TSLA", currentDate, positive_scans)

        body = "---This bot took " + str((time.time() - start_time)/60) + " Minutes to run.---"
        
        if(config.SEND_EMAIL):
            EmailResults.SendMessage(body, "BOT LOG")
        else:
            print(body)

        return positive_scans


if __name__ == '__main__':
    try:
        mainObj().main_func()
        
    except Exception as e:
        if(config.SEND_EMAIL):
            err_msg = str(e)
            EmailResults.SendMessage(err_msg, "BOT LOG")
        else:
            print(e)
    