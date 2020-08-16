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
from testing import *
from csv import writer 
from decimal import Decimal
import os.path
from dataCollector import DataCollector
# insert at 1, 0 is the script path (or '' in REPL)
#FOR LINUX
sys.path.insert(1, config.REPO_FOLDER_LOCATION)


###########################
# THIS IS THE MAIN SCRIPT #
###########################

class mainObj:

    def __init__(self):
        pass



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
        
        data.reset_index(level=0, inplace=True)
        is_outlier = data['Volume'] > upper_limit
        is_in_three_days = ((currentDate - data['Date']) <= datetime.timedelta(days=config.DAY_CUTTOFF))
        return data[is_outlier & is_in_three_days]

    def customPrint(self, d, tick, RSI):
        print("\n\n\n*******  " + tick.upper() + "  *******")
        print("Ticker: "+tick.upper())
        print("RSI: "+str(RSI))
        print("*********************\n\n\n")

    def getRSI(self, data):
        ticker_df = data.reset_index()
        df = ticker_df
        df['RSI'] = RSI_Calc.computeRSI(df['Adj Close'], config.DAYS_OF_RSI)
        
        #print("\n"+ str(df.iloc[-1]["RSI"]))
        return df

    def checkForEntryPoint(self, data):
        rowCount = len(data.index)
        
        if(rowCount>3):
            fast_ema=float(data.iloc[-1]["fast_EMA"])
            slow_ema=float(data.iloc[-1]["slow_EMA"])
            
            RSI=float(data.iloc[-1]["RSI"])
            prev_RSI = float(data.iloc[-2]["RSI"])
            prev_fast_ema=float(data.iloc[-2]["fast_EMA"])
            prev_slow_ema=float(data.iloc[-2]["slow_EMA"])
            if(  prev_fast_ema < prev_slow_ema and fast_ema > slow_ema and RSI > float(config.HIGH_RSI_POINT) ):
                print("BUY")
                return True
            elif(prev_fast_ema > prev_slow_ema and fast_ema < slow_ema and RSI < float(config.LOW_RSI_POINT)):
                print("SELL")
                return False
            else:
                return False
        else:
             return False
        



    def parallel_wrapper(self,x, currentDate, positive_scans):
        try:
            Stock_data = DataCollector.getStockData(x)
        
            df = self.getRSI(Stock_data)
            if(not 'RSI' in df.columns):
                return

            df = EMA_Calc.computeEMA(df, "fast_EMA", config.fast_ema_days)
            df = EMA_Calc.computeEMA(df, "slow_EMA", config.slow_ema_days)
            entry_point = self.checkForEntryPoint(df)
        
            #if(not entry_point):
            #    return
            print(df)
            RSI = df.iloc[-1]["RSI"]
            print("\n"+ str(RSI))
        
            RSI_Calc.Price_Graph(df)
        
            self.customPrint(df, x, RSI)
            if(config.SEND_EMAIL):
                EmailResults.SendResults(x, config.send_to, RSI)
            #Allows you to keep all data for the end of the Bots run. Not doing anything with it yet
            stonk = dict()
            stonk['date'] = df['Date'].iloc[-1] 
            stonk['stock'] = x
            stonk['Adj Close'] = df['Adj Close'].iloc[-1]
            
            print(stonk['date'])
            Testing.log_stock_pick_CSV(stonk)
            positive_scans.append(stonk)

        except Exception as e:
            print("Exception occurred in Parallel_wrapper: "+ e)
        
        
        
    def main_func(self):

        positive_scans=True
        StocksController = NasdaqController(True)
        list_of_tickers = StocksController.getList()
        currentDate = datetime.datetime.strptime(
            date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        start_time = time.time()
        if(config.SEND_EMAIL):
            EmailResults.SendMessage("Bot started working", "BOT LOG", config.send_to_log_email)
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
            self.parallel_wrapper("TSLA", currentDate, positive_scans)
        
        body=""
        if(os.path.isfile(R'data\botAnalysisHistory.csv')):
            yesterdays_score = Testing.backTestYesterdaysResults()
            body = "Yesterdays score was a " + str(yesterdays_score) + "!"
        body += "\n---This bot took " + str((time.time() - start_time)/60) + " Minutes to run.---"
        
        if(config.SEND_EMAIL):
            EmailResults.SendMessage(body, "BOT LOG", config.send_to_log_email)
        else:
            print(body)
        print(len(positive_scans))
        #self.writeToCsv(positive_scans)
        return positive_scans


if __name__ == '__main__':
    try:
        mainObj().main_func()


    except Exception as e:
        if(config.SEND_EMAIL):
            err_msg = str(e)
            EmailResults.SendMessage(err_msg, "BOT LOG", config.send_to_log_email)
        else:
            print(e)
    