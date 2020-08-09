import matplotlib.pyplot as plt
import config
import pandas as pd
from market_scanner import mainObj
class EMA_Calc:
    
    def __init__(self):
        pass
   
    def computeSMA(df,  SMA_days):
        df = df.dropna()        # diff in one field(one day)
        df["SMA"] = df["Adj Close"].rolling(SMA_days).mean();
        print(df)
        return df
   
    def computeEMA(data, EMA_days):
        data["EMA"] = data["Adj Close"].ewm(span=EMA_days,min_periods=0,adjust=False,ignore_na=False).mean()
        print(data)

