

#-----------------------------------------------


def data_cleaning(df):

    df = df.fillna(0)

    # Converting everything to upper case
    df = df.apply(lambda x: x.astype(str).str.upper())

    # Editing Column Names
    df.columns = map(str.upper, df.columns)
    df.columns = df.columns.str.replace(' ','_')

    # Changing datatype of columns
    df["DATE"] = pd.to_datetime(df["DATE"],format='%d-%m-%Y')
    df["OPEN"] = pd.to_numeric(df["OPEN"])
    df["HIGH"] = pd.to_numeric(df["HIGH"])
    df["LOW"] = pd.to_numeric(df["LOW"])
    df["CLOSE"] = pd.to_numeric(df["CLOSE"])
    df["ADJUSTED_CLOSE"] = pd.to_numeric(df["ADJUSTED_CLOSE"])
    df["VOLUME"] = pd.to_numeric(df["VOLUME"])

    df = df.sort_values(["DATE"],ascending=[False]).drop_duplicates()

    df = df[df["VOLUME"] > 0]


    df["OPEN - LOW"] = (df["OPEN"] - df["LOW"])/df["OPEN"]
    df["HIGH - OPEN"] = (df["HIGH"] - df["OPEN"])/df["OPEN"]

    df["HIGH - CLOSE"] = (df["HIGH"] - df["CLOSE"])/df["CLOSE"]
    df["CLOSE - LOW"] = (df["CLOSE"] - df["LOW"])/df["CLOSE"]

    df["CLOSE - OPEN"] = (df["CLOSE"] - df["OPEN"])/df["OPEN"]

    df = df.reset_index(drop=True)

    return df


#------------------------------------------------

for stock in nse_stocks.keys():
    nse_stocks[stock] = data_cleaning(nse_stocks[stock])











