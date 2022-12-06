


def bullish_maribozu(df):

    condition = (abs(df["OPEN - LOW"]) < 0.001) & (abs(df["HIGH - CLOSE"]) < 0.001)

    return condition[0]


def bearish_maribozu(df):

    condition = (abs(df["HIGH - OPEN"]) < 0.001) & (abs(df["CLOSE - LOW"]) < 0.001)

    return condition[0]


def spinning_top(df):

    # Red
    condition1 = (df["CLOSE - OPEN"] <= 0) & (df["CLOSE - OPEN"] > -0.01) & (df["HIGH - OPEN"] > 0.01) & (df["CLOSE - LOW"] > 0.01)

    # Blue
    condition2 = (df["CLOSE - OPEN"] < 0.01) & (df["HIGH - CLOSE"] > 0.01) & (df["OPEN - LOW"] > 0.01)

    return (condition1[0] or condition2[0])


def doji(df):

    # Red
    condition1 = (df["CLOSE - OPEN"] <= 0) & (df["CLOSE - OPEN"] > -0.001) & (df["HIGH - OPEN"] > 0.01) & (df["CLOSE - LOW"] > 0.01)

    # Blue
    condition2 = (df["CLOSE - OPEN"] < 0.001) & (df["HIGH - CLOSE"] > 0.01) & (df["OPEN - LOW"] > 0.01)

    return (condition1[0] or condition2[0])



def paper_umbrella_hammer(df):

    # Red - Shadow to Real Body Ratio
    condition1 = abs(df["HIGH - OPEN"]/df["CLOSE - OPEN"]) > 2

    # Blue - Shadow to Real Body Ratio
    condition2 = abs(df["HIGH - CLOSE"]/df["CLOSE - OPEN"]) > 2

    return (condition1[0] or condition2[0])


def paper_umbrella_hanging_man(df):

    # Red - Shadow to Real Body Ratio
    condition1 = abs(df["CLOSE - LOW"]/df["CLOSE - OPEN"]) > 2

    # Blue - Shadow to Real Body Ratio
    condition2 = abs(df["OPEN - LOW"]/df["CLOSE - OPEN"]) > 2

    return (condition1[0] or condition2[0])


def shooting_star(df):

    # Red - Shadow to Real Body Ratio
    condition = (abs(df["HIGH - OPEN"]/df["CLOSE - OPEN"]) > 2) & (df["CLOSE - LOW"] < 0.001)

    # Blue - Shadow to Real Body Ratio
    condition = (abs(df["HIGH - CLOSE"]/df["CLOSE - OPEN"]) > 2) & (df["OPEN - LOW"] < 0.001)

    return condition[0]



#----------------------------------------------


single_candlestick_patterns_strategies_df = pd.DataFrame(nse_stocks.keys())
single_candlestick_patterns_strategies_df.columns = ["STOCK"]



single_candlestick_patterns_strategies_list = ["bullish_maribozu","bearish_maribozu",
                                                "spinning_top","doji",
                                                "paper_umbrella_hammer",
                                                "paper_umbrella_hanging_man",
                                                "shooting_star"]


for col in single_candlestick_patterns_strategies_list:
    single_candlestick_patterns_strategies_df[col] = [eval(col)(nse_stocks[x]) for x in single_candlestick_patterns_strategies_df["STOCK"]]



single_candlestick_patterns_strategies_df["TOTAL"] = single_candlestick_patterns_strategies_df.sum(axis=1)
single_candlestick_patterns_strategies_df = single_candlestick_patterns_strategies_df[single_candlestick_patterns_strategies_df["TOTAL"] > 0]
single_candlestick_patterns_strategies_df = single_candlestick_patterns_strategies_df.sort_values(["TOTAL"],ascending=False)


