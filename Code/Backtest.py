

def backtest_sell(df,nse_stocks_original):

    for i in df.index:

        symbol = df.loc[i,"STOCK"]

        df.loc[i,"HIGH"] = nse_stocks_original[symbol]["HIGH"][0]
        df.loc[i,"LOW"] = nse_stocks_original[symbol]["LOW"][0]
        df.loc[i,"OPEN"] = nse_stocks_original[symbol]["OPEN"][0]
        df.loc[i,"CLOSE"] = nse_stocks_original[symbol]["CLOSE"][0]


    df["ACTUAL ENTRY"] = df[["ENTRY","OPEN"]].min(axis=1)
    df["ACTUAL EXIT"] = df[["EXIT","CLOSE"]].max(axis=1)
    df["ACTUAL EXIT"] = df[["ACTUAL EXIT","STOPLOSS"]].min(axis=1)


    df["PROFIT/LOSS"] = df["ACTUAL ENTRY"] - df["ACTUAL EXIT"]

    return df




def backtest_buy(df,nse_stocks_original):

    for i in df.index:

        symbol = df.loc[i,"STOCK"]

        df.loc[i,"HIGH"] = nse_stocks_original[symbol]["HIGH"][0]
        df.loc[i,"LOW"] = nse_stocks_original[symbol]["LOW"][0]
        df.loc[i,"OPEN"] = nse_stocks_original[symbol]["OPEN"][0]
        df.loc[i,"CLOSE"] = nse_stocks_original[symbol]["CLOSE"][0]


    df["ACTUAL ENTRY"] = df[["ENTRY","OPEN"]].max(axis=1)
    df["ACTUAL EXIT"] = df[["EXIT","CLOSE"]].min(axis=1)
    df["ACTUAL EXIT"] = df[["ACTUAL EXIT","STOPLOSS"]].max(axis=1)


    df["PROFIT/LOSS"] = df["ACTUAL EXIT"] - df["ACTUAL ENTRY"]

    return df



#---------------------------------------------------------------------


for d in range(1,30,1):

    print("\nDay " + str(d) + ": ")

    nse_stocks_actual = nse_stocks.copy()

    for stock in nse_stocks.keys():
        nse_stocks[stock] = nse_stocks[stock].shift(-1)


    buy_profit = 0
    buy_investment = 0

    sell_profit = 0
    sell_investment = 0

    filename = path_code + "Single_Candlestick_Patterns_Strategies.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

    filename = path_code + "Multiple_Candlestick_Patterns_Strategies.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

    filename = path_code + "Filter_Buy_Sell_Stocks.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

    try:

        df = identify_buy_stocks(buy_stocks, nse_stocks)

        df = df.iloc[:3,:]

        df = backtest_buy(df,nse_stocks_actual)

        display(df)


        buy_investment = buy_investment + df["ACTUAL ENTRY"].sum()
        buy_profit = buy_profit + df["PROFIT/LOSS"].sum()

        print("\n\tTotal Buy Investment: " + str(buy_investment))
        print("\tTotal Buy Profit: " + str(buy_profit))
        print("\t% Buy Profit: " + str((buy_profit/buy_investment)*100))
    
    except:
        pass


    try:

        df = identify_sell_stocks(sell_stocks, nse_stocks)

        df = df.iloc[:3,:]

        df = backtest_sell(df,nse_stocks_actual)

        display(df)

        sell_investment = sell_investment + df["ACTUAL ENTRY"].sum()
        sell_profit = sell_profit + df["PROFIT/LOSS"].sum()

        print("\n\tTotal Sell Investment: " + str(sell_investment))
        print("\tTotal Sell Profit: " + str(sell_profit))
        print("\t% Sell Profit: " + str((sell_profit/sell_investment)*100))
    
    except:
        pass

    total_investment = buy_investment + sell_investment
    total_profit = buy_profit + sell_profit

    print("\n\tTotal Investment: " + str(total_investment))
    print("\tTotal Profit: " + str(total_profit))
    print("\t% Profit: " + str((total_profit/total_investment)*100))



















