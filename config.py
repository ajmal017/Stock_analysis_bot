#Set these params to true when running bot. False For Testing
RUN_BOT = True
SEND_EMAIL = True
UPDATE_STOCK_LIST=True

send_to='email@gmail.com'
send_to_log_email = 'email@gmail.com'

#Standard Deviation Cutoff Periods
MONTH_CUTTOFF = 5 #Amount of months of data to analyze
DAY_CUTTOFF = 3 #Look for the past _ days
STD_CUTTOFF = 10 # Number of deviations

DAYS_OF_RSI = 14 #Days of RSI
HIGH_RSI_POINT=60
LOW_RSI_POINT=40
GRAPH_FILE_NAME = R'data/RSI_graph.png'
PATH_TO_STOCK_LIST="data/alllisted.txt"
OTHER_LISTED_PATH="data/otherlisted.txt"
NASDAQ_LISTED_PATH="data/nasdaqlisted.txt"
EXCLUDED_STOCK_PATH="data/excluded.txt"
STOCK_RESULTS = R'data/botAnalysisHistory.csv'
REPO_FOLDER_LOCATION='/home/pi/Documents/Stock_analyzer_bot'

#SMA
fast_sma_days = 5
slow_sma_days = 10


#EMA
fast_ema_days = 13 
slow_ema_days = 49



#Emoji Codes
FIRE = u"\U0001F525"
ICE = u"\U0001F9CA"
NEUTRAL_FACE=u"\U0001F610"

#Testing
DAYS_OF_TEST=5