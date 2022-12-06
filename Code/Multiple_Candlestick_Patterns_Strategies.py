


def bullish_engulfing_pattern(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] < 0)

    condition2 = (df["CLOSE - OPEN"][0] > 0)

    condition3 = ((abs(df["CLOSE - OPEN"][0]) - abs(df["CLOSE - OPEN"].shift(-1)[0])) > 0.01)

    condition4 = (df.shift(-1)["CLOSE"][0] > df["OPEN"][0]) & (df.shift(-1)["OPEN"][0] < df["CLOSE"][0])

    return condition1 & condition2 & condition3 & condition4


def bearish_engulfing_pattern(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] > 0)

    condition2 = (df["CLOSE - OPEN"][0] < 0)

    condition3 = ((abs(df["CLOSE - OPEN"][0]) - abs(df["CLOSE - OPEN"].shift(-1)[0])) > 0.01)

    condition4 = (df.shift(-1)["OPEN"][0] > df["CLOSE"][0]) & (df.shift(-1)["CLOSE"][0] < df["OPEN"][0])

    return condition1 & condition2 & condition3 


def bearish_engulfing_pattern_plus_doji(df):

    condition = bearish_engulfing_pattern(df[1:].reset_index(drop=True)) & doji(df)

    return condition


def piercing_pattern(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] < 0)

    condition2 = (df["CLOSE - OPEN"][0] > 0)

    dummy = np.where(abs(df["CLOSE - OPEN"].shift(-1)[0]) > 0, abs(df["CLOSE - OPEN"][0])/abs(df["CLOSE - OPEN"].shift(-1)[0]),0)
    condition3 = (0.5 < dummy < 1)

    condition4 = (df.shift(-1)["CLOSE"][0] > df["OPEN"][0]) & (df.shift(-1)["OPEN"][0] < df["CLOSE"][0])

    return condition1 & condition2 & condition3 & condition4



def dark_cloud_cover(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] > 0)

    condition2 = (df["CLOSE - OPEN"][0] < 0)

    dummy = np.where(abs(df["CLOSE - OPEN"].shift(-1)[0]) > 0,abs(df["CLOSE - OPEN"][0])/abs(df["CLOSE - OPEN"].shift(-1)[0]),0)
    condition3 = (0.5 < dummy < 1)

    condition4 = (df.shift(-1)["OPEN"][0] > df["CLOSE"][0]) & (df.shift(-1)["CLOSE"][0] < df["OPEN"][0])

    return condition1 & condition2 & condition3 


def bullish_harami_pattern(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] < 0)

    condition2 = (df["CLOSE - OPEN"][0] > 0)

    condition3 = (df.shift(-1)["CLOSE"][0] < df["OPEN"][0]) & (df.shift(-1)["OPEN"][0] < df["CLOSE"][0])

    return condition1 & condition2 & condition3


def bearish_harami_pattern(df):

    condition1 = (df["CLOSE - OPEN"].shift(-1)[0] > 0)

    condition2 = (df["CLOSE - OPEN"][0] < 0)

    condition3 = (df.shift(-1)["OPEN"][0] < df["CLOSE"][0]) & (df.shift(-1)["CLOSE"][0] < df["OPEN"][0])

    return condition1 & condition2 & condition3 


def morning_star(df):

    condition1 = (df.shift(-2)["CLOSE - OPEN"][0] < 0)

    condition2 = (df.shift(-2)["CLOSE"][0] > df.shift(-1)["OPEN"][0])

    condition3 = (df.shift(-1)["CLOSE - OPEN"][0] > 0)

    condition4 = spinning_top(df.shift(-1)) or doji(df.shift(-1))

    condition5 = (df["CLOSE - OPEN"][0] > 0)

    condition6 = (df["OPEN"][0] < df.shift(-1)["CLOSE"][0])

    condition7 = (df["CLOSE"][0] > df.shift(-2)["OPEN"][0])

    return condition1 & condition2 & condition3 & condition4 & condition5 & condition6 & condition7


def evening_star(df):

    condition1 = (df.shift(-2)["CLOSE - OPEN"][0] > 0)

    condition2 = (df.shift(-2)["CLOSE"][0] < df.shift(-1)["OPEN"][0])

    condition3 = (df.shift(-1)["CLOSE - OPEN"][0] < 0)

    condition4 = spinning_top(df.shift(-1)) or doji(df.shift(-1))

    condition5 = (df["CLOSE - OPEN"][0] < 0)

    condition6 = (df["OPEN"][0] < df.shift(-1)["CLOSE"][0])

    condition7 = (df["CLOSE"][0] < df.shift(-2)["OPEN"][0])

    return condition1 & condition2 & condition3 & condition4 & condition5 & condition6 & condition7


#-----------------------------------------------------


multiple_candlestick_patterns_strategies_df = pd.DataFrame(nse_stocks.keys())
multiple_candlestick_patterns_strategies_df.columns = ["STOCK"]



multiple_candlestick_patterns_strategies_list = ["bullish_engulfing_pattern","bearish_engulfing_pattern",
                                                "bearish_engulfing_pattern_plus_doji",
                                                "piercing_pattern","dark_cloud_cover",
                                                "bullish_harami_pattern","bearish_harami_pattern",
                                                "morning_star","evening_star"]


for col in multiple_candlestick_patterns_strategies_list:
    multiple_candlestick_patterns_strategies_df[col] = [eval(col)(nse_stocks[x]) for x in multiple_candlestick_patterns_strategies_df["STOCK"]]


multiple_candlestick_patterns_strategies_df["TOTAL"] = multiple_candlestick_patterns_strategies_df.sum(axis=1)
multiple_candlestick_patterns_strategies_df = multiple_candlestick_patterns_strategies_df[multiple_candlestick_patterns_strategies_df["TOTAL"] > 0]
multiple_candlestick_patterns_strategies_df = multiple_candlestick_patterns_strategies_df.sort_values(["TOTAL"],ascending=False)

















