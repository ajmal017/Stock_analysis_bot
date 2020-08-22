from ftplib import FTP
import os
import errno
import config
from finviz.helper_functions.save_data import export_to_db, export_to_csv
from finviz.screener import Screener
from finviz.main_func import *
import csv
exportList = []


class NasdaqController:
    def getList(self):
        return exportList

    def __init__(self, update=True):

        filters = ['exch_Any', 'idx_Any','geo_usa','sh_price_u50','avgvol_o50'] 
        print("Filtering stocks..")
        stock_list = Screener(filters=filters, order='ticker')
        stock_list.to_csv('data/stocks.csv')
        
        #print(stock_list)
        with open('data/stocks.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')        
            for row in csv_reader:
                global exportList
                exportList.append(row[1])

