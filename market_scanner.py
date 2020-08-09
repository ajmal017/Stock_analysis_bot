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
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pi/Documents/UnusualVolumeDetector-master/data')



###########################
# THIS IS THE MAIN SCRIPT #
###########################

# Change variables to your liking then run the script



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
        #global config.MONTH_CUTTOFF
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
        #global config.STD_CUTTOFF
        #global config.DAY_CUTTOFF
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

    def days_between(self, d1, d2):
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)


    def getRSI(self, data):
        #config.DAYS_OF_RSI = 40
        #start_time = (datetime.datetime.now().date()- timedelta(days=config.DAYS_OF_RSI)).isoformat()
        #end_time = datetime.datetime.now().date().isoformat()         # today
        
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
        EmailResults.SendResults(x, d, RSI)
        stonk = dict()
        stonk['Ticker'] = x
        stonk['TargetDate'] = d['Date'].iloc[0]
        stonk['TargetVolume'] = d['Volume'].iloc[0]
        stonk['RSI'] = RSI
        positive_scans.append(stonk)


        


    def computeRSI(self, data, time_window):
        diff = data.diff(1).dropna()        # diff in one field(one day)

        #this preservers dimensions off diff values
        up_chg = 0 * diff
        down_chg = 0 * diff
    
        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[ diff>0 ]
    
        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[ diff < 0 ]
    
        # check pandas documentation for ewm
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
        # values are related to exponential decay
        # we set com=time_window-1 so we get decay alpha=1/time_window
        up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
        rs = abs(up_chg_avg/down_chg_avg)
        rsi = 100 - 100/(1+rs)
        return rsi


    def main_func(self):
        positive_scans=True
        StocksController = NasdaqController(True)
        list_of_tickers = StocksController.getList()
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        start_time = time.time()
        if(config.SEND_EMAIL):
            #EmailResults.SendMessage("Bot started working")
            print("")
        else:
            print("Bot started working")   

        manager = multiprocessing.Manager()
        positive_scans = manager.list()


        if(config.RUN_BOT):
            with parallel_backend('loky', n_jobs=multiprocessing.cpu_count()):
                Parallel()(delayed(self.parallel_wrapper)(x, currentDate, positive_scans)
                           for x in tqdm(list_of_tickers, miniters=1))
        else:
            self.parallel_wrapper("TSLA", currentDate, positive_scans)

      
        body = "---This bot took " + str((time.time() - start_time/60)) + " Minutes to run.---"
        
        if(config.SEND_EMAIL):
            EmailResults.SendMessage(body)
        else:
            print(body)

        return positive_scans


if __name__ == '__main__':
    try:
        mainObj().main_func()
        
    except Exception as e:
        if(config.SEND_EMAIL):
            EmailResults.SendEmailMessage(e)
        else:
            print(e)
    
    
    
    


"""
Some legacy code down below





























    def find_anomalies(self, data, cutoff):
        data_std = np.std(data['Volume'])
        data_mean = np.mean(data['Volume'])
        anomaly_cut_off = data_std * cutoff
        upper_limit = data_mean + anomaly_cut_off
        indexs = data[data['Volume'] > upper_limit].index.tolist()
        outliers = data[data['Volume'] > upper_limit].Volume.tolist()
        index_clean = [str(x)[:-9] for x in indexs]
        d = {'Dates': index_clean, 'Volume': outliers}
        return d
"""
