import os
import time
import yfinance as yf
import dateutil.relativedelta
from datetime import date, timedelta, datetime
import datetime
import sys
from stocklist import NasdaqController
from RSI_Calc import *
import config
import sys
from RSI_Calc import *
from EMA_Calc import *
from csv import writer
from decimal import Decimal
import os.path
import csv
from dataCollector import *


class Testing:
    
    def __init__(self):
        pass
   
    def backTestYesterdaysResults():
        
        i=0
        score=0
        stockCount=0
        with open(config.STOCK_RESULTS) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:

                if(len(row)>0 and i>=1):
                    csv_date= datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')
                    check_date = csv_date + datetime.timedelta(days=1)
                    in_date_range = ((datetime.datetime.today() - csv_date) <= timedelta(days=config.DAYS_OF_TEST))
                    print(testing_days_ago)
                    
                    if(in_date_range):
                        data = DataCollector.getStockData(row[1])
                        d = data.loc[check_date]
                        print(d)
                        todays_price = float(d["Adj Close"])
                        stockCount+=1
                        yesterday_price= float(row[2])
                        if(yesterday_price > todays_price): 
                            print("Bad Prediction")
                        elif(todays_price > yesterday_price):
                            print("I was correct")
                            score+=1
                i+=1
        score=(score/stockCount)*100
        print(score)
        return score
                    
                #line_count += 1


    def writeToCsv(data):
        fields=['date','stock', 'Adj Close', ]
        for v in data:
            print(v)
        fileName=config.STOCK_RESULTS
        try:
            with open(fileName, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for d in data:
                    writer.writerow(d)
        except IOError:
            print("I/O error")

    def append_list_as_row(data):
        fields=['date','stock', 'Adj Close', ]
        print(type(data))
        
        fileName=config.STOCK_RESULTS
        try:
            with open(fileName, 'a+', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
#                writer.writeheader()
                writer.writerow(data)
        except IOError:
            print("I/O error")


