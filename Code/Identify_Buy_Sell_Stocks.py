


def merge_params(df,nse_stocks):

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

        if(support < 0):
            df = df.drop(index=[i])

    return df 


def identify_sell_stocks(sell_stocks, nse_stocks):  

    df = pd.DataFrame(np.unique(sell_stocks))
    df.columns = ["STOCK"]

    df = merge_params(df,nse_stocks)

    df = filter_stocks_sell(df)

    df["ENTRY"] = df["CLOSE"]
    df["EXIT"] = df["SUPPORT"]
    df["STOPLOSS"] = df["CLOSE"] + (0.05*df["CLOSE"])

    df = df[["STOCK","ENTRY","EXIT","STOPLOSS"]]

    return df


def identify_buy_stocks(buy_stocks, nse_stocks):  

    df = pd.DataFrame(np.unique(buy_stocks))
    df.columns = ["STOCK"]

    df = merge_params(df,nse_stocks)

    df = filter_stocks_buy(df)

    df["ENTRY"] = df["CLOSE"]
    df["EXIT"] = df["RESISTANCE"]
    df["STOPLOSS"] = df["CLOSE"] - (0.05*df["CLOSE"])

    df = df[["STOCK","ENTRY","EXIT","STOPLOSS"]]

    return df

