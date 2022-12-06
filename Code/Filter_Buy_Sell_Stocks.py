
def strategy_filter_stocks(nse_stocks,df,strategy):

    df = df[df[strategy] == True]
    df = df[["STOCK"]].reset_index(drop=True)

    for i in df.index:

        symbol = df.loc[i,"STOCK"]

        df.loc[i,"HIGH"] = nse_stocks[symbol]["HIGH"][0]
        df.loc[i,"LOW"] = nse_stocks[symbol]["LOW"][0]
        df.loc[i,"OPEN"] = nse_stocks[symbol]["OPEN"][0]
        df.loc[i,"CLOSE"] = nse_stocks[symbol]["CLOSE"][0]
        df.loc[i,"VOLUME"] = nse_stocks[symbol]["VOLUME"][0]

        df.loc[i,"10 DAY AVG VOLUME"] = nse_stocks[symbol]["VOLUME"][1:11].mean()

        try:
            support, resistance = support_resistance(symbol,nse_stocks)

            df.loc[i,"SUPPORT"] = support
            df.loc[i,"RESISTANCE"] = resistance
        except:
            df = df.drop(index=[i])
    
    try:
        df = df[df["SUPPORT"] > 0].reset_index(drop=True)
    except:
        pass

    return df


def filter_stocks_sell(df):

    df = df[df["CLOSE"] > df["SUPPORT"]]
    df = df[df["VOLUME"] > df["10 DAY AVG VOLUME"]]

    df["% MAX FALL EXPECTED"] = (df["CLOSE"] - df["SUPPORT"])/df["CLOSE"]


    df = df.sort_values(["% MAX FALL EXPECTED"],ascending=False)
    df = df.reset_index(drop=True)

    return df


def filter_stocks_buy(df):

    df = df[df["CLOSE"] < df["RESISTANCE"]]
    df = df[df["VOLUME"] > df["10 DAY AVG VOLUME"]]

    df["% MAX RISE EXPECTED"] = (df["RESISTANCE"] - df["CLOSE"])/df["CLOSE"]


    df = df.sort_values(["% MAX RISE EXPECTED"],ascending=False)
    df = df.reset_index(drop=True)

    return df

#----------------------------------------------------------

def identify_sell_stock_names(sell_stocks, nse_stocks, df, strategy):

    df = strategy_filter_stocks(nse_stocks,df,strategy)
    try:
        df = filter_stocks_sell(df)

        df = df[df["% MAX FALL EXPECTED"] > 0.5]

        sell_stocks = sell_stocks + list(df["STOCK"])
    except:
        pass

    return sell_stocks



def identify_buy_stock_names(buy_stocks, nse_stocks, df, strategy):

    df = strategy_filter_stocks(nse_stocks,df,strategy)
    try:
        df = filter_stocks_buy(df)

        df = df[df["% MAX RISE EXPECTED"] > 0.5]

        buy_stocks = buy_stocks + list(df["STOCK"])
    except:
        pass

    return buy_stocks


#------------------------------------------------------------------


sell_strategies_single_candlestick = ["bearish_maribozu","paper_umbrella_hanging_man","shooting_star"]


sell_strategies_multiple_candlestick = ["bearish_engulfing_pattern","bearish_engulfing_pattern_plus_doji","dark_cloud_cover",
                                        "bearish_harami_pattern","evening_star"]


buy_strategies_single_candlestick = ["bullish_maribozu","paper_umbrella_hammer"]


buy_strategies_multiple_candlestick = ["bullish_engulfing_pattern","piercing_pattern","bullish_harami_pattern",
                                        "morning_star"]


#------------------------------------------------------------------------


sell_stocks = []

for strategy in sell_strategies_single_candlestick:
    sell_stocks = identify_sell_stock_names(sell_stocks, nse_stocks, single_candlestick_patterns_strategies_df, strategy)

for strategy in sell_strategies_multiple_candlestick:
    sell_stocks = identify_sell_stock_names(sell_stocks, nse_stocks, multiple_candlestick_patterns_strategies_df, strategy)

#----------------------------------------------------------

buy_stocks = []

for strategy in buy_strategies_single_candlestick:
    buy_stocks = identify_buy_stock_names(buy_stocks, nse_stocks, single_candlestick_patterns_strategies_df, strategy)
    

for strategy in buy_strategies_multiple_candlestick:
    buy_stocks = identify_buy_stock_names(buy_stocks, nse_stocks, multiple_candlestick_patterns_strategies_df, strategy)



























