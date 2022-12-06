
#-----------------------------------------------------

scrape_stocks = input("Do you want to scrape stocks? (Y/N)")

backtest = input("Do you want to Backtest? (Y/N")

#----------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
from os.path import dirname

import pandas_market_calendars as mcal
from pandas.tseries.offsets import CustomBusinessDay


from sklearn.linear_model import LinearRegression
from scipy.signal import savgol_filter

import warnings
warnings.filterwarnings("ignore")

#-----------------------------------------------

path = dirname(os.getcwd())

path_source_files = path + "/Source Files/"
path_code = path + "/Code/"


#----------------------------------------------------

if(scrape_stocks == "Y"):
    filename = path_code + "Yahoo_scraper.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

#---------------------------------------------------------

filename = path_code + "Input_Source_Files.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

filename = path_code + "Data_Cleaning.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

filename = path_code + "Support_Resistance.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

filename = path_code + "Identify_Buy_Sell_Stocks.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

#---------------------------------------------------------

nse_stocks_original = nse_stocks.copy()

#------------------------------------------------------------

if(backtest == "Y"):
    filename = path_code + "Backtest.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

#---------------------------------------------------------------


nse_stocks = nse_stocks_original.copy()

#--------------------------------------------------------------


filename = path_code + "Single_Candlestick_Patterns_Strategies.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

filename = path_code + "Multiple_Candlestick_Patterns_Strategies.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

filename = path_code + "Filter_Buy_Sell_Stocks.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))



df = identify_buy_stocks(buy_stocks, nse_stocks)

df = df.iloc[:3,:]

buy_df = df.copy()

display("Buy",buy_df)

#-------------------------------------------------------

df = identify_sell_stocks(sell_stocks, nse_stocks)

df = df.iloc[:3,:]
sell_df = df.copy()


display("Sell",sell_df)







