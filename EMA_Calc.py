import matplotlib.pyplot as plt
import config
import pandas as pd
#import datetime
from datetime import date, timedelta, datetime


class EMA_Calc:
    
    def __init__(self):
        pass
   
    def computeSMA(df, column_name,  SMA_days):
        df = df.dropna()        # diff in one field(one day)
        df[column_name] = df["Adj Close"].rolling(SMA_days).mean();
        #print(df)
        return df
   
    def computeEMA(data, column_name, EMA_days):
        
        data[column_name] = data["Adj Close"].ewm(span=EMA_days,min_periods=0,adjust=False,ignore_na=False).mean()
        #print(data)
        return data


