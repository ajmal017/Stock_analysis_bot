import matplotlib.pyplot as plt
import config
import pandas as pd
import matplotlib.dates as mpl_dates


class RSI_Calc:
    
    
    def __init__(self):
        pass



    
    def computeRSI(data, time_window):
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

    def RSI_Graph(df):
        try:
                      # plot price
            #plt.figure(figsize=(15,5))
            #plt.plot(df['Date'], df['Adj Close'])
            #plt.title('Price chart (Adj Close)')
            #plt.show()

            # plot correspondingRSI values and significant levels
            fig = plt.figure(figsize=(15,5))
            fig.title('RSI chart')
            fig.plot(df['Date'], df['RSI'])
            fig.axhline(0, linestyle='--', alpha=0.1)
            fig.axhline(20, linestyle='--', alpha=0.5)
            fig.axhline(30, linestyle='--')

            fig.axhline(60, linestyle='--')
            fig.axhline(40, linestyle='--', alpha=0.5)
            fig.axhline(100, linestyle='--', alpha=0.1)
            fig.savefig(config.GRAPH_FILE_NAME)
            plt.close(fig)
            
        except Exception as e:
            print(e)



    def Price_Graph(df):
        try:
                      # plot price
            df.index = pd.to_datetime(df.index)
            plt.figure(figsize=(15,5))
            plt.plot(df['Date'], df['Adj Close'], color="black", label="Adj Close")
            plt.plot(df['Date'], df['slow_EMA'], color="red", label="Slow EMA")
            plt.plot(df['Date'], df['fast_EMA'], color="green", label="Fast EMA")
            plt.title('Price chart (Adj Close)')
            plt.legend(loc="upper left")
            plt.savefig(config.GRAPH_FILE_NAME)
            
            
        except Exception as e:
            print(e)